from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from user.models import  Client, Freelancer
from user.serializers import FreelancerSerializer, ClientSerializer, CreateClientSerializer



class ClientAPIView(APIView):
    permission_classes = [IsAdminUser,]

    def get(self, request):
        users = Client.objects.all()
        serializer = ClientSerializer(users, many=True)
        return Response(data=serializer.data)


    @swagger_auto_schema(request_body=CreateClientSerializer)
    def post(self, request):
        serializer = CreateClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class FreelancerAPIView(APIView):
    permission_classes = [IsAdminUser,]

    def get(self, request):
        users = Freelancer.objects.all()
        serializer = FreelancerSerializer(users, many=True)
        return Response(data=serializer.data)


    @swagger_auto_schema(request_body=FreelancerSerializer)
    def post(self, request):
        serializer = FreelancerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)