from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email')
        model = User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio')
        model = User


class CustomTokenObtainSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'confirmation_code')
        model = User

