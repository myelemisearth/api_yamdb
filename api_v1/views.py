from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.core.management.utils import get_random_secret_key
from django.db.models import Avg
from django_filters.rest_framework.backends import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from api_yamdb.settings import EMAIL_FROM, EMAIL_SUBJ, EMAIL_TEXT
from .filters import TitleFilter
from .models import Review, Title, Genre, Category
from .permissions import ReadOnly, IsAdmin, IsModerator, IsOwner
from .serializers import (TitlesSerializerGet, TitlesSerializerPost,
                          UserSerializer, EmailSerializer,
                          CustomTokenObtainSerializer, ReviewSerializer,
                          CommentSerializer, GenresSerializer,
                          CategoriesSerializer)

User = get_user_model()


class CreateDelListViewset(CreateModelMixin, DestroyModelMixin,
                           ListModelMixin, GenericViewSet):
    pass


class UsersViewset(ModelViewSet):
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('username',)

    @action(detail=False, methods=('GET', 'PATCH',),
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        user_id = self.request.user.id
        user = get_object_or_404(User, id=user_id)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
        else:
            serializer = self.get_serializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        return Response(serializer.data)

    def perform_create(self, serializer):
        password = str(get_random_secret_key())[:10]
        password_hash = make_password(password)
        serializer.save(password=password_hash, is_active=True)


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
            EMAIL_TEXT[0].format(email=email, confirm_code=password_hash),
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
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
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


class CategoriesViewSet(CreateDelListViewset):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdmin|ReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenresViewSet(CreateDelListViewset):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdmin|ReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitlesViewset(ModelViewSet):
    permission_classes = (IsAdmin|ReadOnly,)
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitlesSerializerGet
        return TitlesSerializerPost
