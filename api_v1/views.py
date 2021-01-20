from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.core.management.utils import get_random_secret_key
from django_filters.rest_framework.backends import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import (IsAuthenticated, BasePermission,
                                        SAFE_METHODS)
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .filters import TitleFilter
from .models import Review, Comment, Titles, Genres, Categories
from .permissions import ReadOnly, IsAdmin, IsModerator, IsOwner
from .serializers import (TitlesSerializerGet, TitlesSerializerPost,
                          UserSerializer, EmailSerializer,
                          CustomTokenObtainSerializer, ReviewSerializer,
                          CommentSerializer, GenresSerializer,
                          CategoriesSerializer)


from django.db.models import Avg

User = get_user_model()

EMAIL_FROM = 'api_yamdb@yamdb.ru'
EMAIL_SUBJ = 'Thank you for registering on API YamDB'
EMAIL_TEXT = 'Dont reply on this email!!! You just registered on API YamDB ' \
             'with email {email}. For getting your token and using our API ' \
             'send POST request to auth/token/ with email and confirmation_' \
             'code {confirm_code}. Token will return in response body.'


class UsersViewset(ModelViewSet):
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('username',)

    def perform_create(self, serializer):
        password = str(get_random_secret_key())[:10]
        password_hash = make_password(password)
        serializer.save(password=password_hash, is_active=True)


class UserView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj


class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = EmailSerializer

    def perform_create(self, serializer):
        email = serializer.validated_data['email']
        username = email.split('@')[0]
        password = str(get_random_secret_key())[:10]
        password_hash = make_password(password)
        send_mail(
            EMAIL_SUBJ,
            EMAIL_TEXT.format(email=email, confirm_code=password_hash),
            EMAIL_FROM,
            [email],
            fail_silently=False,
        )
        serializer.save(
            username=username, password=password_hash, email=email)


class TokenObtainView(TokenViewBase):
    serializer_class = CustomTokenObtainSerializer


class ReviewsViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated|ReadOnly,
        IsOwner|IsAdmin|IsModerator|ReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated|ReadOnly,
        IsOwner|IsAdmin|IsModerator|ReadOnly,)

    def get_queryset(self):
        reviews = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return reviews.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class CustomViewSet(CreateModelMixin, DestroyModelMixin,
                    ListModelMixin, GenericViewSet):
    pass


class CategoriesViewSet(CustomViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdmin|ReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenresViewSet(CustomViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdmin|ReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitlesViewset(ModelViewSet):
    permission_classes = (IsAdmin|ReadOnly,)
    queryset = Titles.objects.all()
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitlesSerializerGet
        return TitlesSerializerPost
