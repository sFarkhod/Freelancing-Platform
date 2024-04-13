from django.db import models
from datetime import datetime, timedelta
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
import uuid

VIA_EMAIL, VIA_PHONE = ('via_email', 'via_phone')
    
PHONE_EXPIRE = 2
EMAIL_EXPIRE = 5


class BaseModel(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_time']
        abstract = True


class Client(BaseModel):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.DO_NOTHING, related_name='clients')
    company = models.CharField(max_length=255, null=False, blank=False)
    phone_number = models.CharField(max_length=13, null=True, blank=True, unique=True)
    photo = models.ImageField(upload_to='users/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','heic','heif'])])
    bio = models.TextField()
    country = models.CharField(max_length=255, null=False, blank=False)
    city = models.CharField(max_length=255, null=False, blank=False)
    street1 = models.CharField(max_length=255, null=True, blank=True)
    street2 = models.CharField(max_length=255, null=True, blank=True)
    balance = models.CharField(max_length=255, null=True, blank=True)
    # credit_card = models.ForeignKey('payment.Credit_Card', on_delete=models.DO_NOTHING)
    # review = models.ForeignKey('job.Review', on_delete=models.DO_NOTHING)
    # job = models.ForeignKey('job.Job', on_delete=models.DO_NOTHING)


class Freelancer(BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, blank=False,related_name='freelancers')
    company = models.CharField(max_length=255, null=False, blank=False)
    phone_number = models.CharField(max_length=13, null=True, blank=True, unique=True)
    photo = models.ImageField(upload_to='users/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','heic','heif'])])
    bio = models.TextField()
    country = models.CharField(max_length=255, null=False, blank=False)
    city = models.CharField(max_length=255, null=False, blank=False)
    street1 = models.CharField(max_length=255, null=True, blank=True)
    street2 = models.CharField(max_length=255, null=True, blank=True)
    balance = models.CharField(max_length=255, null=True, blank=True)
    # credit_card = models.ForeignKey('payment.Credit_Card', on_delete=models.DO_NOTHING)
    # review = models.ForeignKey('job.Review', on_delete=models.DO_NOTHING)
    # project = models.ForeignKey('job.Job', on_delete=models.DO_NOTHING)



class Confirmation(BaseModel):
    TYPE_CHOICES = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
    )
    code = models.CharField(max_length=4)
    verify_type = models.CharField(max_length=31, choices=TYPE_CHOICES, default=VIA_EMAIL)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verify_codes')
    expiration_time = models.DateTimeField(null=True)
    is_isconfirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.__str__())
    
    def save(self, *args, **kwargs):
        if self.verify_type == VIA_EMAIL:
            self.expiration_time = datetime.now()+timedelta(minutes=EMAIL_EXPIRE)
        else:
            self.expiration_time = datetime.now()+timedelta(minutes=PHONE_EXPIRE)
        super(Confirmation, self).save(*args, **kwargs)
