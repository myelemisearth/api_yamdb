from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.core.management.utils import get_random_secret_key
from django_filters.rest_framework.backends import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import generics, filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenViewBase

from .models import Review, Comment, Titles, Genres, Categories
from .permissions import IsAdmin, IsModerator, IsUser, IsOwnerOrReadOnly
from .serializers import (UserSerializer, EmailSerializer,
                          CustomTokenObtainSerializer, ReviewSerializer,
                          CommentSerializer, TitlesSerializer,
                          GenresSerializer, CategoriesSerializer)

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
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
 
    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        return title.reviews

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get('review_id'))
        return title.comments

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, title=title)


class CategoriesViewset(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)
    search_fields = ('name',)
    lookup_field = 'slug' 


class GenresViewset(ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)
    search_fields = ('name',)
    lookup_field = 'slug' 

class TitlesViewset(ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = PageNumberPagination
