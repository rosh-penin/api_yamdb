from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from rest_framework import serializers, validators

from reviews.models import Category, Genre, Title, Review, Comment
from api_yamdb.settings import MAX_SCORE_VALUE, MIN_SCORE_VALUE


class CustomSlugField(serializers.RelatedField):
    """Custom field for inheriting."""

    def to_representation(self, value):
        return {
            'name': value.name,
            'slug': value.slug
        }

    def to_internal_value(self, data):
        Obj = self.Meta.model
        assert isinstance(data, str), 'Value must be string'
        try:
            return Obj.objects.get(slug=data)
        except Obj.DoesNotExist:
            raise serializers.ValidationError(
                'Object with this slug value does not exist.'
            )


class CategorySlugField(CustomSlugField):
    """Custom field for category field correct work."""
    queryset = Category.objects.all()

    class Meta:
        model = Category


class GenreSlugField(CustomSlugField):
    """Custom field for genre field correct work."""
    queryset = Genre.objects.all()

    class Meta:
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre model."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Serializer for Title model."""
    category = CategorySlugField()
    genre = GenreSlugField(many=True)
    rating = serializers.SerializerMethodField(read_only=True)
    description = serializers.CharField(required=False)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )

    def get_rating(self, obj):
        """Score field is calculated to show average score."""
        score = obj.reviews.aggregate(Avg('score')).get('score__avg')
        if score is not None:
            score = round(score, 1)

        return score

    def validate_year(self, value):
        """Year should not be higher than current year."""
        if value > datetime.now().year:
            raise serializers.ValidationError('Back to the future. Error')

        return value


class ValueFromViewKeyword:
    """
    Custom class to get default value by the key in serializer`s 'view'
    context dictionary.
    """
    requires_context = True

    def __init__(self, context_key):
        self.key = context_key

    def __call__(self, serializer_field):
        return serializer_field.context.get('view').kwargs.get(self.key)

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())
    score = serializers.IntegerField(
        validators=[
            MinValueValidator(
                limit_value=MIN_SCORE_VALUE,
                message='You can`t rate less then 1!'
            ),
            MaxValueValidator(
                limit_value=MAX_SCORE_VALUE,
                message='You can`t rate more then 10!'
            )
        ],
    )
    title = serializers.HiddenField(
        default=ValueFromViewKeyword('title_id')
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
            'title',
        )
        read_only_fields = ('pub_date',)
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title'],
                message='You can`t rate twice!'
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',)
        read_only_fields = ('pub_date',)
