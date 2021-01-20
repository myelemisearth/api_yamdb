from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.validators import UniqueTogetherValidator

from .models import User, Review, Comment, Categories, Genres, Titles


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
                {'detail': 'User doesnt exists or blocked or ' \
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


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Titles
        fields = '__all__'
        read_only_fields = ('rating',)


class TitlesSerializerGet(TitleSerializer):
    genre = GenresSerializer(many=True)
    category = CategoriesSerializer()


class TitlesSerializerPost(TitleSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all(),
        required=False
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects.all(),
        many=True
    )
