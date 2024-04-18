from django.db import models
from user.models import Freelancer, Client


class RequiredSkill(models.Model):
    name = models.CharField(max_length=100)


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


class Proposal(models.Model):
    title = models.CharField(max_length=255)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    proposal_text = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    proposal_date = models.DateTimeField(auto_now_add=True)
    project_lengs = models.CharField(max_length=255)


class Offer(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField(default=0)
    payment_type = models.CharField(max_length=144, choices=PAYMENT_TYPES)
    project_lengs = models.CharField(max_length=255)
    required_skills = models.ForeignKey(RequiredSkill, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    proposals = models.ForeignKey(Proposal, on_delete=models.CASCADE)


class Contract(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    contract_text = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
