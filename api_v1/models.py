from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import custom_year_validator


class User(AbstractUser):

    class Roles(models.TextChoices):
        USR = 'user', ('user')
        MOD = 'moderator', ('moderator')
        ADM = 'admin', ('admin')
    
    email = models.EmailField(
        error_messages={
            'unique': ('A user with that email already exists.'),
        },
        unique=True,
        verbose_name='Почтовый адрес'
    )
    bio = models.TextField(
        max_length=1000,
        blank=True,
        verbose_name='Информация о пользователе'
    )
    role = models.CharField(
        max_length=25,
        choices=Roles.choices,
        default=Roles.ADM,
        verbose_name='Роль'
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)


    @property
    def is_admin(self):
        return self.role == self.Roles.ADM
    
    @property
    def is_moderator(self):
        return self.role == self.Roles.MOD

    @property
    def is_user(self):
        return self.role == self.Roles.USR

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи' 


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=40,
        unique=True,
        verbose_name='Метка'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории' 
        ordering = ('name',)


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=40,
        unique=True,
        verbose_name='Метка'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры' 
        ordering = ('name',)


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название'
    )
    year = models.IntegerField(
        verbose_name='Год',
        validators=[custom_year_validator]
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titles',
        verbose_name='Жанр'
    )

    def get_genre(self):
        return '\n'.join([p.genre for p in self.genre.all()])

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения' 
 
 
class Review(models.Model):
    text = models.TextField(
        verbose_name='Текст'
    )
    score = models.IntegerField(
        default=5,
        validators=[
        MaxValueValidator(10),
        MinValueValidator(1)
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензии' 
        ordering = ('-pub_date',)
 
 
class Comment(models.Model):
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        blank=True,
        null=True,
        verbose_name='Рецензия'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии' 
        ordering = ('-pub_date',)
