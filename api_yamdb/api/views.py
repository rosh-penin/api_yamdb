from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework import permissions
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title, Review
from users.models import User
from .filters import TitleFilters
from .permissions import (
    IsAdminOrReadOnly,
    IsAdminOrModerOrAuthorOrReadOnly,
    IsAdmin
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleSerializerPostUpdate,
    ReviewSerializer,
    CommentSerializer,
    UserSerializer,
    SignUpSerializer,
    CustomTokenObtainSerializer
)

EMAIL_FROM = 'no-reply@example.com'


def get_access_token(user):
    """Get user object and return the access token."""
    refresh = RefreshToken.for_user(user)
    return {'token': str(refresh.access_token)}


def get_object(self, keyword, model):
    return get_object_or_404(model, pk=self.kwargs.get(keyword))


class BaseViewSet(CreateModelMixin, DestroyModelMixin,
                  ListModelMixin, GenericViewSet):
    """ViewSet for inheriting. Pre-configured some stuff."""
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter, )
    search_fields = ('name',)


class CategoryViewSet(BaseViewSet):
    """ViewSet for Category model."""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'


class GenreViewSet(BaseViewSet):
    """ViewSet for Genre model."""
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class TitleViewSet(ModelViewSet):
    """ViewSet for Title model."""
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.all()
    filterset_class = TitleFilters

    def get_serializer_class(self):
        if self.action not in ('list', 'retrieve'):
            return TitleSerializerPostUpdate

        return TitleSerializer


class ReviewViewSet(ModelViewSet):
    """ViewSet for Review model."""
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = (IsAdminOrModerOrAuthorOrReadOnly, )

    def get_queryset(self):
        title = get_object(self, 'title_id', Title)
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object(self, 'title_id', Title)
        if self.request.user.reviews.filter(title=title):
            raise ValidationError('You already posted review to this title')
        serializer.save(
            author=self.request.user,
            title=title)


class CommentViewSet(ModelViewSet):
    """ViewSet for Comment model."""
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrModerOrAuthorOrReadOnly, )

    def get_queryset(self):
        review = get_object(self, 'review_id', Review)

        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object(self, 'review_id', Review)
        serializer.save(
            author=self.request.user,
            review=review)


class UsersSignUp(APIView):
    """Allows users to get confirmation code to their email.
    If user with specified username and email doesn't exist,
    the new account will be created.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        email = serializer.data.get('email')
        user, created = User.objects.get_or_create(username=username,
                                                   email=email)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Ваш код для получения токена. ',
            f'Здравствуйте, {username}! Ваш код для получения токена: '
            f'{confirmation_code}',
            EMAIL_FROM,
            [email],
            fail_silently=False
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersTokenObtain(APIView):
    """User can send his username
    and confirmation code and receive authentication token.
    """
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
        raise serializers.ValidationError({'confirmation_code': 'is invalid'})


class UserViewSet(ModelViewSet):
    """Admin or superuser can manage users. The 'me' action allows users
    to get the information about himself or modify this information.
    """
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    @action(methods=['get', 'patch'], detail=False,
            permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        if request.method == 'PATCH':
            serializer = self.get_serializer(request.user, data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
