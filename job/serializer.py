from rest_framework import serializers
from .models import Job, RequiredSkill, Proposal, Offer, Contract
from user.serializers import FreelancerSerializerApiView, ClientSerializerApiView


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequiredSkill
        fields = ['id', 'name']


class JobSerializer(serializers.ModelSerializer):
    # required_skills = SkillsSerializer(many=True)
    job_client = ClientSerializerApiView(read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'price', 'payment_type', "job_client", 'project_length',
                  'required_skills']


class JobListSerializer(serializers.ModelSerializer):
    required_skills = SkillsSerializer(many=True)
    job_client = ClientSerializerApiView(read_only=True)

    class Meta:
        model = Job
        fields = "__all__"


class ProposalSerializer(serializers.ModelSerializer):
    freelancer = FreelancerSerializerApiView(read_only=True)

    class Meta:
        model = Proposal
        fields = "__all__"


class ProposalListSerializer(serializers.ModelSerializer):
    freelancer = FreelancerSerializerApiView(read_only=True)
    job = JobSerializer(read_only=True)

    class Meta:
        model = Proposal
        fields = "__all__"


class ProposalSerializerForPatchingClient(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = ["watched", ]


class ProposalSerializerForPatchingClientForClose(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = ["close_feedback", ]


class OfferSerializer(serializers.ModelSerializer):
    freelancer = FreelancerSerializerApiView(read_only=True)
    client = ClientSerializerApiView(read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'project_lengs', 'client', 'freelancer', 'extra_information', 'proposals',
                  'price', 'is_active', 'upload_file', 'contract']


class OfferSerializerForClose(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['is_active', ]


class ContractSerializer(serializers.ModelSerializer):
    offer = OfferSerializer(read_only=True)

    class Meta:
        model = Contract
        fields = "__all__"


class ContractSerializerForFreelancer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['sign_img', ]
