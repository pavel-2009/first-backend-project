from django.urls import reverse

from ..models import Post
from .fixtures import PostFixturesTest


class PostCreateFormTest(PostFixturesTest):

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        # Подсчитаем количество записей в Post
        post_count = Post.objects.count()
        form_data = {
            'text': 'Тестовая запись поста при тестирование формы',
            'author': self.user,
            'group': self.group.pk,
        }
        # Отправляем POST-запрос
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(
            response, reverse(
                'posts:profile', kwargs={'username': self.user}
            )
        )
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), post_count + 1)
        # проверяем, создался ли пост, который мы заказывали.
        # проверим что text, автор и группа совпадает.
        self.assertTrue(
            Post.objects.filter(
                text='Тестовая запись поста при тестирование формы',
                author=self.user,
                group=self.group.pk,
            ).exists()
        )

    def test_edit_post(self):
        """Валидная форма обновляет запись в Post."""
        form_data = {
            'text': 'Измененная запись поста',
            'author': self.user,
        }
        # Отправляем POST-запрос
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True,
        )
        # проверяем изменился ли text
        self.assertEqual(
            Post.objects.filter(id=self.post.id).last().text,
            form_data['text']
        )
        # проверяем, сработал ли редирект
        self.assertRedirects(
            response, reverse(
                'posts:post_detail', kwargs={'post_id': self.post.id}
            )
        )
