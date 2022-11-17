from datetime import datetime

from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment


class CustomSlugField(serializers.RelatedField):

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
    queryset = Category.objects.all()

    class Meta:
        model = Category


class GenreSlugField(CustomSlugField):
    queryset = Genre.objects.all()

    class Meta:
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySlugField()
    genre = GenreSlugField(many=True)
    rating = serializers.SerializerMethodField(read_only=True)
    description = serializers.CharField(required=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score')).get('score__avg')

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError('Back to the future. Error')

        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )
        read_only_fields = ('pub_date',)


class CommentSerializer(serializers.ModelSerializer):
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
