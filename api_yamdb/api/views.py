from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from reviews.models import Category, Genre, Title, Review
from .filters import TitleFilters
from .permissions import IsAdminOrReadOnly, IsAdminOrModerOrAuthorOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer, ReviewSerializer,
                          CommentSerializer)


class BaseViewSet(CreateModelMixin, DestroyModelMixin,
                  ListModelMixin, GenericViewSet):
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter, )
    search_fields = ('name',)


class CategoryViewSet(BaseViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'


class GenreViewSet(BaseViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class TitleViewSet(ModelViewSet):
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.all()
    filterset_class = TitleFilters


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = (IsAdminOrModerOrAuthorOrReadOnly, )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(
            author=self.request.user,
            title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrModerOrAuthorOrReadOnly, )

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(
            author=self.request.user,
            review=review)
