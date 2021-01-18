from django.shortcuts import get_object_or_404 
from rest_framework import viewsets, filters 
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated
 
from .models import Review, Comment, Title
from .serializers import ReviewSerializer, CommentSerializer 
from .permissions import IsOwnerOrReadOnly 


class ReviewsViewSet(viewsets.ModelViewSet): 
    serializer_class = CommentSerializer 
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly] 
 
    def get_queryset(self): 
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id")) 
        return title.reviews 
 
    def perform_create(self, serializer): 
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id")) 
        serializer.save(author=self.request.user, title=title) 


class CommentsViewSet(viewsets.ModelViewSet): 
    serializer_class = ReviewSerializer 
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly] 
 
    def get_queryset(self): 
        title = get_object_or_404(Title, pk=self.kwargs.get("review_id")) 
        return title.comments 
 
    def perform_create(self, serializer): 
        title = get_object_or_404(Title, pk=self.kwargs.get("review_id")) 
        serializer.save(author=self.request.user, title=title) 
