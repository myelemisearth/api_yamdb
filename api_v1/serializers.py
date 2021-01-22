from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from .models import User, Review, Comment, Category, Genre, Title
from .validators import custom_year_validator

RANGE_ERROR_MESSAGE = 'Entered value must be between 1 and 10'


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    score = serializers.IntegerField(
        validators=(
            MinValueValidator(1, message=RANGE_ERROR_MESSAGE),
            MaxValueValidator(10, message=RANGE_ERROR_MESSAGE),
        )
    )

    def validate(self, data):
        title_id = self.context.get('view').kwargs.get('title_id')
        author = self.context.get('request').user
        if (self.context.get('request').method == 'POST' and
            Review.objects.filter(title_id=title_id,
                                  author_id=author.id).exists()):
            raise serializers.ValidationError(
                {'detail': 'You have already left a review about this title'})
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField()
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Comment


class CustomTokenObtainSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        email = data['email']
        confirmation_code = data['confirmation_code']
        user = User.objects.filter(
            email=email, password=confirmation_code, is_active=1).first()
        if user is None:
            raise serializers.ValidationError(
                {'detail': 'User doesnt exists or blocked or '
                    'confirmation code is incorrect'})
        token = {'token': str(AccessToken.for_user(user))}
        return token


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=User.Roles.choices,
        default='user'
    )

    class Meta:
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'email', 'role')
        model = User


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data['email']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'detail': 'Entered email is exists'})
        return data

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Category


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitlesSerializerGet(TitleSerializer):
    genre = GenresSerializer(many=True)
    category = CategoriesSerializer()


class TitlesSerializerPost(TitleSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    year = serializers.IntegerField(
        required=False,
        validators=(custom_year_validator,)
    )
