from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers, validators

from reviews.models import Category, Genre, Title, Review, Comment
from api_yamdb.settings import MAX_SCORE_VALUE, MIN_SCORE_VALUE
from users.models import User

username_validator = UnicodeUsernameValidator()


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
    """Serializer for Title model. Only for GET requests."""
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    description = serializers.CharField(required=False)
    rating = serializers.IntegerField(read_only=True)

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


class TitleSerializerPostUpdate(TitleSerializer):
    """Serializer for Title model. POST, PATCH and DELETE requests."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )


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
