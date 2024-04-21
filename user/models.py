from django.db import models
from datetime import datetime, timedelta
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
import random
from rest_framework_simplejwt.tokens import RefreshToken
import uuid
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta


VIA_EMAIL, VIA_PHONE = ('via_email', 'via_phone')
NEW, CODE_VERIFIED = ("new", 'code_verified')
FREELANCER, CLIENT, ADMIN = ("freelancer", 'client', 'admin')
PHONE_EXPIRE = 2
EMAIL_EXPIRE = 5


class BaseModel(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_time']
        abstract = True


class User(AbstractUser, BaseModel):
    USER_TYPES = (
        (FREELANCER, FREELANCER),
        (CLIENT, CLIENT)
    )

    AUTH_TYPE_CHOICE = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
    )

    AUTH_STATUS = (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED)
    )
    user_type = models.CharField(
        max_length=31, choices=USER_TYPES, null=True, blank=True)
    auth_type = models.CharField(max_length=31, choices=AUTH_TYPE_CHOICE, default=VIA_EMAIL)
    auth_status = models.CharField(max_length=31, choices=AUTH_STATUS, default=NEW)
    email = models.EmailField(null=True, blank=True, unique=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True, unique=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def create_verify_code(self, verify_type):
        code = "".join([str(random.randint(0,100) % 10) for _ in range(4)])
        UserConfirmation.objects.create(
            user_id = self.id,
            verify_type = verify_type,
            code = code)
        return code
    
    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access" : str(refresh.access_token),
            "refresh": str(refresh)
        }


class UserConfirmation(BaseModel):
    TYPE_CHOICES = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
    )
    code = models.CharField(max_length=4)
    verify_type = models.CharField(max_length=31, choices=TYPE_CHOICES, default=VIA_EMAIL)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='verify_codes')
    expiration_time = models.DateTimeField(null=True)
    is_isconfirmed = models.BooleanField(default=False)    

    def save(self, *args, **kwargs):
        if self.verify_type == VIA_EMAIL:
            self.expiration_time = datetime.now()+timedelta(minutes=EMAIL_EXPIRE)
        else:
            self.expiration_time = datetime.now()+timedelta(minutes=PHONE_EXPIRE)
        super(UserConfirmation, self).save(*args, **kwargs)


class Client(BaseModel):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.DO_NOTHING, related_name='clients')
    company = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True, unique=True)
    photo = models.ImageField(upload_to='clients/', null=True, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'heif'])])
    bio = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    street1 = models.CharField(max_length=255, null=True, blank=True)
    street2 = models.CharField(max_length=255, null=True, blank=True)
    balance = models.CharField(max_length=255, null=True, blank=True)
    # credit_card = models.ForeignKey('payment.Credit_Card', on_delete=models.DO_NOTHING)
    job = models.ForeignKey('job.Job', null=True, blank=True, on_delete=models.DO_NOTHING)


class Freelancer(BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, blank=False, related_name='freelancers')
    company = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True, unique=True)
    photo = models.ImageField(upload_to='freelancers/', null=True, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'heif'])])
    bio = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    street1 = models.CharField(max_length=255, null=True, blank=True)
    street2 = models.CharField(max_length=255, null=True, blank=True)
    balance = models.CharField(max_length=255, null=True, blank=True)
    # credit_card = models.ForeignKey('payment.Credit_Card', on_delete=models.DO_NOTHING)
    project = models.ForeignKey('job.Job', null=True, blank=True, on_delete=models.DO_NOTHING)


class Feedback(BaseModel):
    comment = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.DO_NOTHING)
    freelancer = models.ForeignKey(Freelancer, null=True, blank=True, on_delete=models.DO_NOTHING)
    stars_given = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])