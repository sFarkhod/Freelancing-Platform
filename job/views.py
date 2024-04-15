from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Job, RequiredSkill
from .serializer import JobSerializer, SkillsSerializer, JobListSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView


# views for job

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
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
# @permission_classes([IsAuthenticated])
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
