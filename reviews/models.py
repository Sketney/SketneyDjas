from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import (MaxValueValidator,
                                    MinValueValidator)
from django.db import models

from api_yamdb.settings import USERNAME_LENGTH
from api.validators import validate_username

LENGTH = 15


class User(AbstractUser):
    """Модель для user."""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]

    username = models.CharField(
        max_length=USERNAME_LENGTH,
        unique=True,
        null=True,
        validators=[UnicodeUsernameValidator(),
                    validate_username],)
    email = models.EmailField(
        'Адрес электронной почты',
        unique=True,
        default='user@example.com',)
    bio = models.TextField(
        'Биография',
        blank=True,
        null=False,)
    role = models.CharField(
        'Роль пользователя',
        max_length=50,
        choices=ROLE_CHOICES,
        default=USER,)

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN


class Category(models.Model):
    """Модель для категорий."""
    name = models.CharField(
        max_length=settings.CHARS_LENGTH,
        verbose_name='название',
        db_index=True
    )
    slug = models.SlugField(
        max_length=settings.SLUG_LENGTH,
        unique=True,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name[:LENGTH]


class Genre(models.Model):
    """Модель для жанров."""
    name = models.CharField(
        verbose_name='название',
        max_length=settings.CHARS_LENGTH,
        db_index=True
    )
    slug = models.SlugField(
        max_length=settings.SLUG_LENGTH,
        verbose_name='slug',
        unique=True,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name[:LENGTH]


class Title(models.Model):
    """Модель для тайтлов."""
    name = models.CharField(
        max_length=settings.CHARS_LENGTH,
        verbose_name='название',
        db_index=True
    )
    year = models.SmallIntegerField(
        verbose_name='год создания',
        validators=[
            MaxValueValidator(
                int(datetime.now().year),
                message='Год не может быть больше нынешнего'
            )
        ],
        db_index=True
    )
    description = models.TextField(
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='жанр',
        help_text='Выберите жанр:',
        blank=False,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        help_text='Выберите категорию:',
        null=True,
        blank=False,
    )

    class Meta:
        ordering = ('-year', 'name')

    def __str__(self):
        return self.name[:LENGTH]


class Review(models.Model):
    """Модель для отзывов."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    text = models.TextField("Текст", help_text="Отзыв")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    score = models.SmallIntegerField(
        verbose_name="Оценка",
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        ordering = ["-pub_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_review"
            )
        ]

    def __str__(self):
        return self.name[:LENGTH]


class Comment(models.Model):
    """Модель для комментариев."""
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField("Текст", help_text="Комментарий")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text
