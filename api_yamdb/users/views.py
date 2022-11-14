from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.decorators import api_view

from .serializers import (UserSerializer,
                          SignUpSerializer,
                          CustomTokenObtainSerializer
                          )

User = get_user_model()


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        confirmation_code = get_random_string(length=32)
        send_mail(
            'Код для получения токена',  # Тема письма.
            f'Код для получения токена: {confirmation_code}',  # Тело письма.
            'from@example.com',  # Это поле "От кого", нужно доработать.
            [f'{serializer.validated_data["email"]}'],  # Это поле "Куда", тут все нормально.
            fail_silently=False,
            # Сообщать об ошибках («молчать ли об ошибках?»)
        )
        serializer.save(confirmation_code=confirmation_code)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view('POST')
def custom_token_obtain(request):
    serializer = CustomTokenObtainSerializer(data=request.data)
    if serializer.is_valid():
        ...



