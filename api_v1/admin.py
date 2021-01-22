from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Comment, Genre, Review, User, Title


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'author', 'text', 'pub_date',)


class GenresAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'text', 'score', 'pub_date',)


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description', 'year',)
    raw_id_fields = ('genre',)
    


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoriesAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenresAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitlesAdmin)
