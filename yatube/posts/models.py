from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Post(models.Model):
    text = models.TextField(
        max_length=4000,
        verbose_name='Описание поста',
        help_text='Введите текст поста',
    )
    pub_date = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_posts",
        verbose_name='Автор',
    )
    group = models.ForeignKey(
        'Group',
        on_delete=models.SET_NULL,
        related_name="group_posts",
        blank=True,
        null=True,
        verbose_name='Группа',
        help_text='Выберите группу',
)
    
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
    )
    
    class Meta:
        ordering = ('-pub_date',)
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.text[:15]


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите текст комментария',
    )
    created = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True,
        db_index=True,      
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
