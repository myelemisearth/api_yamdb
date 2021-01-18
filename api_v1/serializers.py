from rest_framework import serializers 
from rest_framework.validators import UniqueTogetherValidator 
 
from .models import Review, Comment
 
 
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
