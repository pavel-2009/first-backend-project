from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст поста',
        help_text='Введите текст поста'
        )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        help_text='Введите дату публицации поста',
        auto_now_add=True
        )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        help_text='Выберите автора поста',
        on_delete=models.CASCADE,
        related_name='posts',
    )
    group = models.ForeignKey(
        'Group',
        verbose_name='Группа',
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        help_text='Группа, к которой будет относиться пост'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
        help_text='Загрузите картинку'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:15]


class Group(models.Model):
    title = models.CharField(
        verbose_name='Название группы',
        max_length=200,
        help_text='Введите название группы',
        unique=True,
        blank=False, null=False
        )
    slug = models.SlugField(
        unique=True,
        verbose_name='Адрес группы',
        help_text='Введите адрес группы',
        blank=False, null=False
        )
    description = models.TextField(
        verbose_name='Описание группы',
        help_text='Введите описание группы'
    )

    def __str__(self):
        return self.title
