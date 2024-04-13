from django.db import models
from user.models import Freelancer, Client


class RequiredSkill(models.Model):
    name = models.CharField(max_length=100)


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
    project_length = models.IntegerField()
    required_skills = models.ManyToManyField('RequiredSkill')


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



