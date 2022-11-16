from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
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
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=50)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User
