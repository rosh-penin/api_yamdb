from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email')
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Please, use another username to signup')
        return value


class CustomTokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=50)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio')
        model = User

