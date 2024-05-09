from django.contrib import admin
from .models import RequiredSkill, Job, Proposal, Offer


admin.site.register([RequiredSkill, Job, Proposal, Offer])
