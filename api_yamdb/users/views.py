from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework import permissions
from rest_framework import serializers
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

from api.permissions import IsAdmin
from .serializers import (UserSerializer, SignUpSerializer,
                          CustomTokenObtainSerializer)

User = get_user_model()


def get_access_token(user):
    refresh = RefreshToken.for_user(user)
    return {'token': str(refresh.access_token)}


def send_confirmation_code(to_email, confirmation_code):
    subject = 'Ваш код для получения токена.'
    body = f'Код для получения токена: {confirmation_code}'
    from_email = 'no-reply@example.com'
    send_mail(subject, body, from_email, to_email, fail_silently=False)


class UsersSignUp(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        email = serializer.data.get('email')
        user, created = User.objects.get_or_create(username=username,
                                                   email=email)
        confirmation_code = default_token_generator.make_token(user)
        send_confirmation_code([email], confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersTokenObtain(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = CustomTokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            return Response(get_access_token(user),
                            status=status.HTTP_200_OK)
        raise serializers.ValidationError({'confirmation_code': 'is_invalid'})


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    @action(methods=['get', 'patch'], detail=False,
            permission_classes=(permissions.IsAuthenticated,),
            url_path='me', url_name='me')
    def me(self, request):
        if request.method == 'PATCH':
            serializer = self.get_serializer(request.user, data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
