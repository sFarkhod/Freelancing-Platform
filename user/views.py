from rest_framework import permissions
from rest_framework.generics import CreateAPIView, UpdateAPIView
from user.serializers import (SignUpSerializer, LoginSerializer, VerifyCodeSerializer, LoginRefreshSerializer,
                              LogoutSerializer, ForgotPassswordSerializer, ResetPasswordSerializer,
                              FreelancerSerializer, FreelancerUpdateSerializer,
                              ClientSerializer, ClientUpdateSerializer,
                              FeedbackSerializer, NotificationSerializer)  
from user.models import CODE_VERIFIED, NEW, VIA_EMAIL, VIA_PHONE, User, Client, Freelancer, Feedback
from rest_framework.views import APIView
from datetime import datetime
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from drf_yasg.utils import swagger_auto_schema
from user.utility import check_email_username_or_phone, send_email
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404
import requests
from django.shortcuts import redirect
from django.conf import settings
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


class NotificationAPIView(APIView):
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(request_body=NotificationSerializer)
    def post(self, request, *args, **kwargs):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleLoginAPIView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, **kwargs):
        client_id = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
        google_redirect_url = "http://127.0.0.1:8000/user/google/callback"
        return redirect(f"https://accounts.google.com/o/oauth2/auth?client_id={client_id}&redirect_uri={google_redirect_url}&response_type=code&scope=email%20profile")


class GoogleCallbackAPIView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, **kwargs):
        code = request.GET.get('code')
        google_redirect_url = "http://127.0.0.1:8000/user/google/callback"
        response = requests.post('https://oauth2.googleapis.com/token',
            data={
                'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': google_redirect_url
            },
            headers={'Accept': 'application/json'}
        )
        access_token = response.json().get('access_token')
        if access_token:
            profile_endpoint = 'https://www.googleapis.com/oauth2/v1/userinfo'
            headers = {'Authorization': f'Bearer {access_token}'}
            profile_response = requests.get(profile_endpoint, headers=headers)
            if profile_response.status_code == 200:
                data = {}
                profile_data = profile_response.json()
                if User.objects.filter(email=profile_data["email"]).exists():
                    user = User.objects.filter(email=profile_data["email"]).first()
                    refresh = RefreshToken.for_user(user)
                    data['access'] = str(refresh.access_token)
                    data['refresh'] = str(refresh)
                    return Response(data, status.HTTP_201_CREATED)
                user = User.objects.create(username=profile_data["email"].split("@")[0],last_name=profile_data["given_name"], email=profile_data["email"], first_name=profile_data["family_name"])
                refresh = RefreshToken.for_user(user)
                data['access'] = str(refresh.access_token)
                data['refresh'] = str(refresh)
                return Response(data, status.HTTP_201_CREATED)
        return Response({}, status.HTTP_400_BAD_REQUEST)
        

class FeedbackAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(request_body=FeedbackSerializer)
    def post(self, request, *args, **kwargs):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, **kwargs):
        feedbacks = Feedback.objects.all()
        if feedbacks:
            paginator = PageNumberPagination()
            page_obj = paginator.paginate_queryset(feedbacks, request)
            serializer = FeedbackSerializer(page_obj, many=True)
            return paginator.get_paginated_response(serializer.data)
        data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Ma'lumot topilmadi!"
        }
        return Response(data=data)


class FreelancerListAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = FreelancerSerializer

    def get(self, request, **kwargs):
        freelancers = Freelancer.objects.all()
        if freelancers:
            paginator = PageNumberPagination()
            page_obj = paginator.paginate_queryset(freelancers, request)
            serializer = FreelancerSerializer(page_obj, many=True)
            return paginator.get_paginated_response(serializer.data)
        data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Ma'lumot topilmadi!"
        }
        return Response(data=data)


class FreelancerDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = FreelancerSerializer

    def get(self, request, id):
        try:
            freelancer = get_object_or_404(Freelancer, id=id)
            if freelancer:
                serializer = FreelancerSerializer(freelancer)
                data = {
                    "data": serializer.data,
                    "status": status.HTTP_200_OK,
                    "success": True
                }
                return Response(data=data)
        except:
            data = {
                "data": [],
                "status": status.HTTP_404_NOT_FOUND,
                "success": False
                }
            return Response(data=data)


class FreelancerUdateAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = FreelancerUpdateSerializer
    
    @swagger_auto_schema(request_body=FreelancerUpdateSerializer)
    def patch(self, request, id):
        try:
            freelaner = get_object_or_404(Freelancer, id=id)
        except:
            freelaner = None
        if freelaner:
            serializer = FreelancerUpdateSerializer(instance=freelaner, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = {
            "data": [],
            "status": status.HTTP_404_NOT_FOUND,
            "success": False
        }
        return Response(data=data)


class ClientListAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ClientSerializer

    def get(self, request, **kwargs):
        clients = Client.objects.all()
        if clients:
            paginator = PageNumberPagination()
            page_obj = paginator.paginate_queryset(clients, request)
            serializer = ClientSerializer(page_obj, many=True)
            return paginator.get_paginated_response(serializer.data)
        data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Ma'lumot topilmadi!"
        }
        return Response(data=data)


class ClientDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ClientSerializer

    def get(self, request, id):
        try:
            client = get_object_or_404(Client, id=id)
            if client:
                serializer = ClientSerializer(client)
                data = {
                    "data": serializer.data,
                    "status": status.HTTP_200_OK,
                    "success": True
                }
                return Response(data=data)
        except:
            data = {
                "data": [],
                "status": status.HTTP_404_NOT_FOUND,
                "success": False
            }
            return Response(data=data)
        

class ClientUdateAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ClientUpdateSerializer
    
    @swagger_auto_schema(request_body=ClientUpdateSerializer)
    def patch(self, request, id):
        try:
            client = get_object_or_404(Client, id=id)
        except:
            client = None
        if client:
            serializer = ClientUpdateSerializer(instance=client, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = {
            "data": [],
            "status": status.HTTP_404_NOT_FOUND,
            "success": False
        }
        return Response(data=data)


class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = SignUpSerializer


class VerifyAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    @swagger_auto_schema(request_body=VerifyCodeSerializer)
    def post(self, request, *args, **kwargs):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data.get('code')
            user = self.request.user
            self.check_verify(user, code)
            return Response(
                    data = {
                        'status':True,
                        'user_type':user.user_type,
                        "access": user.token()['access'],
                        "refresh": user.token()['refresh']
                    }
                )
    
    @staticmethod
    def check_verify(user, code):
        verifies = user.verify_codes.filter(expiration_time__gte = datetime.now(), code=code, is_isconfirmed=False)
        if not verifies.exists():
            data = {
                "message":"Tasdiqlash kodingiz xato yoki eskirgan"
            }
            raise ValidationError(data)
        verifies.update(is_isconfirmed=True)
        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFIED
            user.save()
            return True
            

class GetNewVerification(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get (self, request, *args, **kwargs):
        user = self.request.user
        self.check_verification(user)
        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user.email, code)
        elif user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_PHONE)
            send_email(user.phone_number, code)
        else:
            data = {
                'message':"Email yoki Phone number xato!"
            }
            raise ValidationError(data)
        return Response(
            {
                'success':True,
                'message':"Tasdiqlash kodingiz qaytadan jo'natildi"
            }
        )
    
    @staticmethod
    def check_verification(user):
        verifies = user.verify_codes.filter(expiration_time__gte = datetime.now(), is_isconfirmed=False)
        if verifies.exists():
            data = {
                'message':"Kodingiz hali ishlatish uchun yaroqli. Biroz kutib turing"
            }
            raise ValidationError(data)
        

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class LoginRefreshView(TokenRefreshView):
    serializer_class = LoginRefreshSerializer


class LogoutView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(request_body=LogoutSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = self.request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            data = {
                "success":True,
                "message":"You are loggout out"
            }
            return Response(data, status=205)
        except TokenError:
            return Response(status=400)


class ForgotPasswordView(APIView):
    serializer_class = ForgotPassswordSerializer
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(request_body=ForgotPassswordSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = self.request.data)
        if serializer.is_valid(raise_exception=True):
            email_address = serializer.validated_data.get('email_address')
            user = serializer.validated_data.get('user')
            if check_email_username_or_phone(email_address) =='phone':
                code = user.create_verify_code(VIA_PHONE)
                send_email(email_address, code)
            if check_email_username_or_phone(email_address) =='email':
                code = user.create_verify_code(VIA_EMAIL)
                send_email(email_address, code)
            return Response(
                {
                    'success': True,
                    'message': "Tasdiqlash kodi muvaffaqiyatli yuborildi!!",
                    'access': user.token()['access'],
                    "refresh": user.token()['refresh'],
                    "user_status": user.auth_status
                }, status=200
            )


class ResetPasswordView(UpdateAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_name = ['patch', 'put']


    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        response = super(ResetPasswordSerializer, self).update(request, *args, **kwargs)
        try:
            user = User.objects.get(id = response.data.get('id'))
        except ObjectDoesNotExist:
            raise NotFound(detail="User not found")
        return Response(
            {
                "success":True,
                "message":"Parolingiz muvaffaqiyatli o'zgartirildi!!!",
                "access":user.token()['access'],
                "access":user.token()['refresh_token'],
            }
        )
