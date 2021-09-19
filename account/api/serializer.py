import jwt
from rest_framework import serializers
from account.models import User
from rest_framework_jwt.serializers import jwt_payload_handler

from django.conf import settings


class UserLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email'
        )


class LoginSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'password', 'token',
        )

    def get_token(self, obj):
        payload = jwt_payload_handler(obj)
        token = jwt.encode(payload, settings.SECRET_KEY)
        return token

    def validate_email(self, value: object) -> object:
        if User.objects.filter(email=value).exists():
            return value
        return serializers.ValidationError('this email is not exist')


class SignUpSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'password', 'phone_number', 'token'
        )

    def get_token(self, obj):
        payload = jwt_payload_handler(obj)
        token = jwt.encode(payload, settings.SECRET_KEY)
        return token

    def validate_email(self, value: object) -> object:
        if User.objects.filter(email=value).exists():
            return serializers.ValidationError('this email is already exist')
        return value

    def create(self, validated_data):
        user =User.objects.create_user(**validated_data)
        return User

class UserProfileSerializer(serializers.ModelSerializer):


class ChangePasswordSerializer(serializers.Serializer):
    OldPassword = serializers.CharField(required=True, max_length=150)
    NewPassword = serializers.CharField(required=True, max_length=150)
    NewPasswordRepeat = serializers.CharField(required=True, max_length=150)

    def validate(self, data):
        old_pass = data.get['OldPassword']
        pass_1 = data.get['NewPassword']
        pass_2 = data.get['NewPasswordRepeat']
        old_pass_check = User.check_password(old_pass)
        if old_pass_check:
            if pass_1 == pass_2:
                User.set_password(pass_1)
            else:
                return serializers.ValidationError('password1 and password2 not the same')
        return serializers.ValidationError('the old password wrong!!')
