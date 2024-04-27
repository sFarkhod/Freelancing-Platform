from rest_framework import serializers
from .models import Job, RequiredSkill, Proposal
from user.serializers import FreelancerSerializerApiView


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequiredSkill
        fields = ['id', 'name']


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'price', 'payment_type', 'project_length', 'required_skills']


class JobListSerializer(serializers.ModelSerializer):
    required_skills = SkillsSerializer(many=True)

    class Meta:
        model = Job
        fields = "__all__"


class ProposalSerializer(serializers.ModelSerializer):
    freelancer = FreelancerSerializerApiView(read_only=True)

    class Meta:
        model = Proposal
        fields = "__all__"
