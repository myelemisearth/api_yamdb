from rest_framework import serializers 
from rest_framework.validators import UniqueTogetherValidator 
from rest_framework_simplejwt.tokens import AccessToken

from .models import User, Review, Comment, Categories, Genres, Titles


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
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
                {'detail': 'User doesnt exists or blocked or' \
                    ' confirmation code is incorrect'})
        token = {'token': str(AccessToken.for_user(user))}
        return token


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.Roles.choices, default='user')

    class Meta:
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'email', 'role')
        model = User


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data['email']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Entered email is exists')
        return data

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(read_only=True, many=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Titles
