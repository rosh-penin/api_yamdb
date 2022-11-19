from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from reviews.models import Category, Genre, Title, Review
from .filters import TitleFilters
from .permissions import IsAdminOrReadOnly, IsAdminOrModerOrAuthorOrReadOnly
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer
)


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
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.all()
    filterset_class = TitleFilters


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
