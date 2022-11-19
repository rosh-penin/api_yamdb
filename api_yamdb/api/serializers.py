from datetime import datetime

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User

username_validator = UnicodeUsernameValidator()


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
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')

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


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""
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


class SignUpSerializer(serializers.Serializer):
    """Check if combination of username and email exists or
    doesn't exist than return the data.
    """
    username = serializers.CharField(max_length=150,
                                     validators=[username_validator])
    email = serializers.EmailField()

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Please, use another username to signup')
        return value

    def validate(self, data):
        users = User.objects.all()
        if users.filter(username=data['username'], email=data['email']):
            return data
        if users.filter(username=data['username']):
            raise serializers.ValidationError({'username': 'already in use'})
        if users.filter(email=data['email']):
            raise serializers.ValidationError({'email': 'already in use'})
        return data


class CustomTokenObtainSerializer(serializers.Serializer):
    """Token obtain serializer."""
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=150)


class UserSerializer(serializers.ModelSerializer):
    """User serializer to serialize the user model."""
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
        model = User
