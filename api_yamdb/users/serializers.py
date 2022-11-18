from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

User = get_user_model()
username_validator = UnicodeUsernameValidator()


class SignUpSerializer(serializers.Serializer):
    """Check if combination of username and email exists or
    doesn't exist than return the data.
    """
    username = serializers.CharField(max_length=150,
                                     validators=[username_validator])
    email = serializers.EmailField()

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Please, use another username to signup')
        return value

    def validate(self, data):
        users = User.objects.all()
        if users.filter(username=data['username'], email=data['email']):
            return data
        if users.filter(username=data['username']):
            raise serializers.ValidationError({'username': 'already in use'})
        if users.filter(email=data['email']):
            raise serializers.ValidationError({'email': 'already in use'})
        return data


class CustomTokenObtainSerializer(serializers.Serializer):
    """Token obtain serializer."""
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=150)


class UserSerializer(serializers.ModelSerializer):
    """User serializer to serialize the user model."""
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
        model = User
