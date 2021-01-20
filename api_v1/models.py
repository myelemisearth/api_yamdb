from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):

    class Roles(models.TextChoices):
        USR = 'user', ('user')
        MOD = 'moderator', ('moderator')
        ADM = 'admin', ('admin')
    
    email = models.EmailField(
        ('email address'),
        error_messages={
            'unique': ('A user with that email already exists.'),
        },
        unique=True
    )
    bio = models.TextField(
        max_length=1000,
        blank=True
    )
    role = models.CharField(
        max_length=9,
        choices=Roles.choices,
        default=Roles.ADM
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    class Meta:
        ordering = ('username',)


class Categories(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True
    )
    slug = models.SlugField(
        max_length=40,
        unique=True
    )

    class Meta:
        ordering = ('name',)


class Genres(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True
    )
    slug = models.SlugField(
        max_length=40,
        unique=True
    )

    class Meta:
        ordering = ('name',)


class Titles(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True
    )
    year = models.IntegerField()
    description = models.TextField()
    rating = models.FloatField()
    category = models.ForeignKey(
        Categories,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genres,
        blank=True,
        related_name='titles'
    )

    class Meta:
        ordering = ('name',)
 
 
class Review(models.Model):
    text = models.TextField()
    score = models.IntegerField(
        default=5,
        validators=[
        MaxValueValidator(10),
        MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField(
        'date published',
        auto_now_add=True
    )
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        ordering = ('author',)
 
 
class Comment(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        ordering = ('author',)
