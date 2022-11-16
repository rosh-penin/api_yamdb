from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from reviews.models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class BaseViewSet(CreateModelMixin, DestroyModelMixin,
                  ListModelMixin, GenericViewSet):
    lookup_field = 'slug'


class CategoryViewSet(BaseViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'


class GenreViewSet(BaseViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class TitleViewSet(ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
