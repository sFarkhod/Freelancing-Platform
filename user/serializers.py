from rest_framework import serializers
from user.models import Client, Freelancer, User
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
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
        fields = ('username', 'email', 'last_name', 'first_name', 'password', 'confirm_password')


class CreateClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Client
        fields = "__all__"

    def create(self, validated_data):
        user_model = validated_data.pop('user')
        user = User(
            username = user_model.get('username'),
            last_name = user_model.get('last_name'),
            first_name = user_model.get('first_name'),
            email = user_model.get('email')
        )
        user.set_password(user_model.get('password'))
        user.save()
        client = Client.objects.create(user=user, **validated_data)
        return client

    def validate(self, data):
        user = data.get('user')
        password = user.get('password', None)
        confirm_password = user.get('confirm_password', None)

        if password:
            validate_password(password)

        if password != confirm_password:
            raise ValidationError(
                {
                    'message': "Parolingiz va tasdiqlash parolingiz bir biriga teng emas"
                }
            )
        return data
    

class ClientSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Client
        fields = ('id','user', 'company')


class FreelancerSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Freelancer
        fields = ('id','user', 'company')
