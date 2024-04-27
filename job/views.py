from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Job, RequiredSkill, Proposal
from .serializer import JobSerializer, SkillsSerializer, JobListSerializer, ProposalSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from user.models import Freelancer

# views for job

class JobPagination(PageNumberPagination):
    page_size = 10


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_job(request):
    try:
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response([e])


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


class ProposalListApiView(ListAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer


class ProposalDetailApiView(APIView):
    def get(self, request, pk):

        try:
            freelancer = Freelancer.objects.get(user=request.user)
            proposal = Proposal.objects.get(pk=pk, freelancer=freelancer)

        except Proposal.DoesNotExist:
            return Response({"message": "Proposal Not Found.!"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProposalSerializer(proposal)

        return Response(serializer.data)







