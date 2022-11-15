from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (UserSerializer,
                          SignUpSerializer,
                          CustomTokenObtainSerializer
                          )

User = get_user_model()


def get_access_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token)
    }


def send_confirmation_code(to_email, confirmation_code):
    subject = 'Ваш код для получения токена.'
    body = f'Код для получения токена: {confirmation_code}'
    from_email = 'no-reply@example.com'
    send_mail(subject, body, from_email, to_email, fail_silently=False)


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        confirmation_code = get_random_string(length=50)
        email = [serializer.validated_data["email"]]
        send_confirmation_code(email, confirmation_code)
        serializer.save(confirmation_code=confirmation_code)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def custom_token_obtain(request):
    serializer = CustomTokenObtainSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data.get('username')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if user.confirmation_code == confirmation_code:
            user.is_active = True
            user.save()
            return Response(get_access_token(user),
                            status=status.HTTP_200_OK)
        return Response({'confirmation_code': 'is invalid'},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer