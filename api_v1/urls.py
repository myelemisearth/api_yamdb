from django.urls import path, include
from rest_framework.routers import DefaultRouter
 
from .views import (UserRegisterView, TokenObtainView, UserView, UsersViewset,
                    ReviewsViewSet, CommentsViewSet,
                    TitlesViewset, GenresViewSet, CategoriesViewSet)
 

router = DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews', 
                ReviewsViewSet, 
                basename='ReviewsViewSet') 
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/',
                CommentsViewSet,
                basename='CommentsViewSet') 
router.register('users',
                UsersViewset,
                basename='users')
router.register(r'titles',
                TitlesViewset,
                basename='titles')
router.register(r'categories',
               CategoriesViewSet,
               basename='categories')
router.register(r'genres',
               GenresViewSet,
               basename='genres')

auth_patterns = [
    path('email/',
         UserRegisterView.as_view()),
    path('token/',
         TokenObtainView.as_view())
]
urlpatterns = [ 
    path('auth/',
         include(auth_patterns)),
    path('users/me/',
         UserView.as_view()),
    path('',
         include(router.urls)),
]