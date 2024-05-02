from django.contrib import admin
from .models import RequiredSkill, Job, Proposal


admin.site.register([RequiredSkill, Job, Proposal])
