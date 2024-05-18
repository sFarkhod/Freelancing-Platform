from django.db import models
from user.models import Freelancer, Client
from django.db.models.signals import post_save
from django.dispatch import receiver


class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class RequiredSkill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


PAYMENT_TYPES = [
    ('fixed', 'Fixed'),
    ('monthly', 'Monthly'),
    ('hourly', 'Hourly'),
]


class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPES)
    project_length = models.CharField(max_length=10)
    required_skills = models.ManyToManyField('RequiredSkill')
    job_client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='jobs_client')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class Proposal(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    project_lengs = models.CharField(max_length=10)
    cover_letter = models.TextField(blank=True, null=True)
    image1 = models.ImageField(upload_to='images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='images/', blank=True, null=True)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    close_feedback = models.TextField(blank=True, null=True)
    job = models.ForeignKey(Job, on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.freelancer.user.username


VALUE_TYPE = (
    ('add_contract', 'add_contract'),
    ('no_contract', 'no_contract')
)


class Offer(models.Model):
    price = models.IntegerField(default=0)
    project_lengs = models.CharField(max_length=255)
    extra_information = models.TextField(blank=True, null=True)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.DO_NOTHING)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    proposals = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    contract = models.CharField(max_length=20, choices=VALUE_TYPE)
    is_active = models.BooleanField(default=True)
    upload_file = models.FileField(upload_to='documents/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Contract(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='offer_for_added_contracts')
    file_path = models.FileField(upload_to='documents/')
    contract_text = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.CharField(max_length=20, blank=True, null=True)
    sign_img = models.ImageField(upload_to='images/', blank=True, null=True)


contract_choice = 'add_contract'


@receiver(post_save, sender=Offer)
def create_contract_on_offer_save(sender, instance, created, **kwargs):
    if created and instance.contract == contract_choice:
        if instance.upload_file:
            Contract.objects.create(
                offer=instance,
                file_path=instance.upload_file
            )
        else:
            Contract.objects.create(
                offer=instance,
                contract_text=instance.proposals.job.description,
                start_date=instance.created_at,
                end_date=instance.project_lengs

            )
