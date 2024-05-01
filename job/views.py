from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Job, RequiredSkill, Proposal
from .serializer import JobSerializer, SkillsSerializer, JobListSerializer, ProposalSerializer, ProposalListSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from user.models import Freelancer, Client
from django.db.utils import IntegrityError


# views for job

class JobPagination(PageNumberPagination):
    page_size = 10


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_job(request):
    if request.user.is_authenticated:
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            job_client = Client.objects.get(user=request.user)
            serializer.save(job_client=job_client)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("ro'yxatdan o't ")


class JobListApiView(ListAPIView):
    queryset = Job.objects.all()
    pagination_class = JobPagination
    serializer_class = JobListSerializer


@api_view(['GET'])
def get_job(request, pk):
    try:
        job = Job.objects.get(pk=pk)

    except Job.DoesNoteExist:
        return Response({"error": "Job Not Found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = JobSerializer(job)
    return Response(serializer.data)


# views for required_skills

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_skill(request):
    try:
        serializer = SkillsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response([e])


class SkillsListApiView(ListAPIView):
    queryset = RequiredSkill.objects.all()
    serializer_class = SkillsSerializer


# views for proposal

class CreateProposalApiView(APIView):

    def post(self, request):
        post_data = request.data
        user = request.user

        try:
            if request.user.is_authenticated:
                if request.user.user_type == 'freelancer':
                    serializer = ProposalSerializer(data=post_data)

                    if serializer.is_valid():
                        freelancer = Freelancer.objects.get(user=user)

                        serializer.save(freelancer=freelancer)
                        return Response(serializer.data)
                    return Response(serializer.errors)

                else:
                    return Response('you can not do this action')

            else:
                return Response('please signup or signin')

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as i:
            return Response({"error": i})


@api_view(['GET'])
def get_my_proposals(request):
    if request.user.is_authenticated:
        freelancer = Freelancer.objects.get(user=request.user)
        proposal = Proposal.objects.filter(freelancer=freelancer)

        if proposal:
            serializer = ProposalListSerializer(proposal, many=True)
            return Response(serializer.data)
        return Response({"message": "You have not any proposal.!"})
    else:
        Response({"error": "User is not authenticated.!"}, status=status.HTTP_401_UNAUTHORIZED)


class ProposalDetailApiView(APIView):
    def get(self, request, pk):

        try:
            if request.user.is_anonymous:
                return Response('loging qiling shaxsingiz aniqlanmadi')

            freelancer = Freelancer.objects.get(user=request.user)
            proposal = Proposal.objects.get(pk=pk, freelancer=freelancer)
            serializer = ProposalListSerializer(proposal)

            return Response(serializer.data)

        except Proposal.DoesNotExist:
            return Response({"message": "Proposal Not Found.!"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_proposal(request, pk):
    try:
        if request.user.is_authenticated:
            freelancer = Freelancer.objects.get(user=request.user)
            proposal = Proposal.objects.get(pk=pk, freelancer=freelancer)

            if proposal:
                proposal.delete()
                return Response({"message": "Proposal was Successfully deleted"})

    except Proposal.DoesNotExist:
        return Response({"error": "Proposal Yo'q xullas (get out here)"},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
def update_proposal(request, pk):
    try:
        if request.user.is_authenticated:
            if request.user.user_type == 'freelancer':
                freelancer = Freelancer.objects.get(user=request.user)
                proposal = Proposal.objects.get(pk=pk, freelancer=freelancer)

                serializer = ProposalSerializer(proposal, data=request.data)

                if serializer.is_valid():
                    serializer.save(freelancer=freelancer)
                    return Response(serializer.data)
                return Response(serializer.errors)

            else:
                return Response('you can not do this action')

        else:
            return Response('please signup or signin')

    except Proposal.DoesNoteExist:
        return Response({"message": "Proposal Not Found"}, status=status.HTTP_404_NOT_FOUND)


# proposal for client

@api_view(['PATCH'])
def patch_proposal_for_client(request, pk):
    if request.user.is_authenticated:
        if request.user.user_type == 'client':
            try:
                proposal = Proposal.objects.get(pk=pk)
                job_proposal = proposal.job.job_client.user
                client = Client.objects.get(user=job_proposal)

                if client == request.user:
                    serializer = ProposalSerializer(proposal, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                    return Response(serializer.errors, status=400)
                else:
                    return Response('Unauthorized access', status=403)

            except (Proposal.DoesNotExist, Client.DoesNotExist):
                return Response('Proposal or Client not found', status=404)

        else:
            return Response('You cannot perform this action', status=403)

    else:
        return Response('Please signup or signin', status=401)












