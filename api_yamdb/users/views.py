from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions

from .serializers import UserSerializer, SignUpSerializer

User = get_user_model()


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        ...


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

