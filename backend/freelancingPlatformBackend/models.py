from django.db import models
from django.contrib.auth.models import User, AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    pass

    country = models.CharField(max_length=100)
    def tokens(self):
        '''Return access and refresh tokens'''
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Freelancer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.CharField(max_length=100)
    bio = models.TextField()
    profile_pic = models.ImageField(upload_to='freelancer_profile_pics/', blank=True)
    street1 = models.CharField(max_length=100)
    street2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField()
    profile_pic = models.ImageField(upload_to='client_profile_pics/', blank=True)
    street1 = models.CharField(max_length=100)
    street2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    PAYMENT_TYPES = [
        ('fixed', 'Fixed'),
        ('monthly', 'Monthly'),
        ('hourly', 'Hourly'),
    ]
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPES)
    project_length = models.IntegerField()  # Duration in days, months, or hours
    required_skills = models.ManyToManyField('RequiredSkill')

class RequiredSkill(models.Model):
    name = models.CharField(max_length=100)

class Feedback(models.Model):
    feedback = models.TextField()
    star = models.IntegerField()

class CreditCard(models.Model):
    cardholder_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)  # Assuming it's a string for simplicity
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=4)  # Assuming CVV is 3 or 4 digits for simplicity

class Withdrawal(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    withdrawal_date = models.DateTimeField(auto_now_add=True)
    freelancer = models.OneToOneField(Freelancer, on_delete=models.CASCADE)

class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)

class Subscription(models.Model):
    TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    freelancer = models.OneToOneField(Freelancer, on_delete=models.CASCADE)

class Proposal(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    proposal_text = models.TextField()
    price_offer = models.DecimalField(max_digits=10, decimal_places=2)
    proposal_date = models.DateTimeField(auto_now_add=True)

class Offer(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    offer_text = models.TextField()
    offer_amount = models.DecimalField(max_digits=10, decimal_places=2)
    offer_date = models.DateTimeField(auto_now_add=True)

class Contract(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    contract_text = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

class WatchedJob(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)