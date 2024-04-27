from rest_framework import serializers
from user.models import Client, Freelancer, User, Feedback, VIA_EMAIL, CODE_VERIFIED
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from user.utility import send_email, check_email_username_or_phone
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.generics import get_object_or_404
from django.contrib.auth.models import update_last_login


class FreelancerSerializerApiView(serializers.ModelSerializer):
    class Meta:
        model = Freelancer
        fields = ['id', 'user']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('user_type', 'username', 'email', 'last_name', 'first_name',)
    

class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Client
        fields = "__all__"


class ClientUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = Client
        fields = ('first_name','last_name', 'username', 'email', 'bio', 'country',
                    'city', 'street1', 'street2', 'balance', 'company', 'phone_number')
    
    def update(self, instance, validated_data):
        username = validated_data.pop('username', '')
        email = validated_data.pop('email', '')
        first_name = validated_data.pop('first_name', '')
        last_name = validated_data.pop('last_name', '')
        instance = super().update(instance, validated_data)
        instance.user.email = email
        instance.user.name = username
        instance.user.last_name = last_name
        instance.user.first_name = first_name
        instance.user.save()
        return instance


class FreelancerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Freelancer
        fields = "__all__"


class FreelancerUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = Freelancer
        fields = ('first_name','last_name', 'username', 'email', 'bio', 'country',
                    'city', 'street1', 'street2', 'balance', 'company', 'phone_number' )
    
    
    def update(self, instance, validated_data):
        username = validated_data.pop('username', '')
        email = validated_data.pop('email', '')
        first_name = validated_data.pop('first_name', '')
        last_name = validated_data.pop('last_name', '')
        instance = super().update(instance, validated_data)
        instance.user.email = email
        instance.user.name = username
        instance.user.last_name = last_name
        instance.user.first_name = first_name
        instance.user.save()
        return instance
        

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True,
        validators=[validate_password]
    )

    confirm_password = serializers.CharField(
        write_only=True, required=True,
        validators=[validate_password]
    )

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('user_type', 'username', 'email', 'last_name', 'first_name', 'password', 'confirm_password')

    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)
        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user.email, code)
        if validated_data.get('password'):
            user.set_password(validated_data.get('password'))
        user.save()
        return user
    

    def validate(self, data):
        password = data.get('password', None)
        email = data.get('email', None)
        confirm_password = data.pop('confirm_password', None)

        if password:
            validate_password(password)
        if confirm_password:
            validate_password(confirm_password)
        if User.objects.filter(email=email).exists():
            data = {
                'succes':False,
                'message':"Bu email address ro'yhatdan o'tkazilgan"
            }
            raise ValidationError(data)
        if password!=confirm_password:
            raise ValidationError(
                {
                    'message':"Parolingiz va tasdiqlash parolingiz bir biriga teng emas"
                }
            )
        return data
    
    def to_representation(self, instance):
        data =super(SignUpSerializer, self).to_representation(instance)
        data = instance.token()
        return data


class VerifyCodeSerializer(serializers.Serializer):
    code =  serializers.CharField(required=True)


class LoginSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.fields['userinput'] = serializers.CharField(required=True)
        self.fields['username'] = serializers.CharField(required=False, read_only = True)

    def auth_validate(self, data):
        user_input = data.get("userinput")
        if check_email_username_or_phone(user_input)=='username':
            username = user_input
        elif check_email_username_or_phone(user_input)=='email':
            user = User.objects.get(email__iexact=user_input)
            username = user.username
        elif check_email_username_or_phone(user_input)=='phone':
            user = User.objects.get(phone_number=user_input)
            username = user.username
        else:
            data = {
                "success": True,
                "message":"Siz email, username yoki telefon raqam jo'natishingiz kerak!"
            }
            raise ValidationError(data)
        
        authectication_kwargs = {
            self.username_field : username,
            'password': data['password']
        }
        current_user = User.objects.filter(username__iexact=username).first()
        if current_user is None:
            raise ValidationError(
                {
                    'success':False,
                    "message": "Bunday foydalanuvchi mavjud emas!"
                }
            )
        if current_user.auth_status != CODE_VERIFIED:
            raise ValidationError(
                {
                    'success':False,
                    "message": "Siz ro'yhatdan to'liq o'tmagansiz."
                }
            )
        user = authenticate(**authectication_kwargs)

        if user is not None:
            self.user = user
        else:
            raise ValidationError(
                {
                'success':False, 
                'message':" Sorry, login or password you entered is incorrect. Please check and try again"
            }
            )
        
    def validate(self, data):
        self.auth_validate(data)
        data = self.user.token()
        data['user_type'] = self.user.user_type
        return data
    

    def get_user(self, **kwargs):
        users = User.objects.filter(**kwargs)
        if not users.exists():
            raise ValidationError(
                {
                    "message":"No active account found"
                }
            )
        return users.first()
    

class LoginRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        access_token_instance = AccessToken(data['access'])
        user_id = access_token_instance['user_id']
        user = get_object_or_404(User, id = user_id)
        update_last_login(None, user)
        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class ForgotPassswordSerializer(serializers.Serializer):
    email_address = serializers.CharField(write_only = True, required = True)

    def validate(self, attrs):
        email_address = attrs.get('email_address', None)
        if email_address is None:
            raise ValidationError(
                {
                    'success':False,
                    "message":"Email yoki telefon raqami kiritilishi shart!"
                }
            )
        user = User.objects.filter(email=email_address).first()
        if user:
            attrs['user'] = user
            return attrs
        else:
            raise NotFound(
                detail = "User not found"
            )


class ResetPasswordSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only = True)
    password = serializers.CharField(write_only=True, required = True)
    confirm_password = serializers.CharField(write_only=True, required = True)

    class Meta:
        model = User
        fields = (
            "id", "password", "confirm_password"
        )

    def validate(self, data):
        password = data.get('password', None)
        confirm_password = data.get('confirm_password', None)
        if password != confirm_password:
            raise ValidationError(
                {
                    "success":False,
                    "message":"Parollaringiz qiymati bir biriga teng emas"
                })
        if password:
            validate_password(password)
        return data

    def update(self, instance, validated_data):
        password = validated_data.pop("password")
        instance.set_password(password)
        return super(ResetPasswordSerializer, self).update(instance, validated_data)