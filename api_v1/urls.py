from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import ( 
        TokenObtainPairView, 
        TokenRefreshView, 
    ) 
 
from .views import ReviewsViewSet, CommentsViewSet
 

v1_router = DefaultRouter()
v1_router.register(r'titles/(?P<title_id>\d+)/reviews', 
                   ReviewsViewSet, 
                   basename='ReviewsViewSet') 
v1_router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/',
                   CommentsViewSet,
                   basename='CommentsViewSet') 
 
 
urlpatterns = [ 
    path('v1/', include(v1_router.urls)), 
    path( 
        'token/', 
        TokenObtainPairView.as_view(), 
        name='token_obtain_pair'), 
    path( 
        'token/refresh/', 
        TokenRefreshView.as_view(), 
        name='token_refresh'), 
]
