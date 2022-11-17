from django_filters import ModelMultipleChoiceFilter, FilterSet, CharFilter
from reviews.models import Category, Genre, Title


class TitleFilters(FilterSet):
    genre = ModelMultipleChoiceFilter(
        field_name='genre__slug',
        to_field_name='slug',
        queryset=Genre.objects.all()
    )
    category = ModelMultipleChoiceFilter(
        field_name='category__slug',
        to_field_name='slug',
        queryset=Category.objects.all()
    )
    name = CharFilter(lookup_expr='contains')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'year', 'name')
