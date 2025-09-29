from django import test

from posts.models import Post, Group, User
from django.urls import reverse


class PostFormTests(test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser')
        cls.group = Group.objects.create(
            title='Test Group',
            slug='test-group',
            description='A group for testing'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Initial post text',
            group=cls.group
        )

    def setUp(self):
        self.client = test.Client()
        self.client.force_login(self.user)

    def test_post_create_valid_form(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'New post text',
            'group': self.group.id
        }
        self.client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )

        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(Post.objects.filter(text='New post text',
                                            group=self.group).exists())

    def test_post_edit_valid_form(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Updated post text',
            'group': self.group.id
        }
        self.client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True
        )

        self.assertEqual(Post.objects.count(), posts_count)
        self.post.refresh_from_db()
        self.assertEqual(self.post.text, 'Updated post text')
        self.assertEqual(self.post.group, self.group)

    def test_invalid_forms(self):
        posts_count = Post.objects.count()
        invalid_form_data = [
            {'text': '', 'group': self.group.id},
            {'text': 'Valid text', 'group': 9999},  # Non-existent group
        ]

        for form_data in invalid_form_data:
            with self.subTest(form_data=form_data):
                response = self.client.post(
                    reverse('posts:post_create'),
                    data=form_data
                )
                self.assertEqual(response.status_code, 200)
                self.assertFormError(
                    response,
                    'form',
                    'text',
                    'Обязательное поле.' if form_data['text'] == ''
                    else None)
                self.assertEqual(Post.objects.count(), posts_count)

                response = self.client.post(
                    reverse('posts:post_edit',
                            kwargs={'post_id': self.post.id}),
                    data=form_data
                )
                self.assertEqual(response.status_code, 200)
                self.assertFormError(
                    response,
                    'form',
                    'text',
                    'Обязательное поле.' if form_data['text'] == ''
                    else None)
                self.assertEqual(Post.objects.count(), posts_count)

    def test_post_create_no_group(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Post without group',
            'group': ''
        }
        self.client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )

        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(Post.objects.filter(text='Post without group',
                                            group__isnull=True).exists())
        
    def test_post_create_with_author(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Post with author',
            'group': self.group.id
        }
        self.client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )

        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(Post.objects.filter(text='Post with author',
                                            author=self.user).exists())
        
    def test_post_edit_change_author(self):
        new_user = User.objects.create_user(username='newuser')
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Attempt to change author',
            'group': self.group.id,
            'author': new_user.id
        }
        self.client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True
        )

        self.assertEqual(Post.objects.count(), posts_count)
        self.post.refresh_from_db()
        self.assertEqual(self.post.author, self.user)
        self.assertNotEqual(self.post.author, new_user)

    def test_templatetags_context(self):
        """Проверка контекста шаблонов с использованием templatetags."""
        response = self.client.get(reverse('posts:index'))
        self.assertIn('page_obj', response.context)

        response = self.client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        )
        self.assertIn('page_obj', response.context)
        self.assertIn('text', response.context)
        self.assertIn('group', response.context)

        response = self.client.get(
            reverse('posts:profile', kwargs={'username': self.user.username})
        )
        self.assertIn('page_obj', response.context)
        self.assertIn('username', response.context)
        self.assertIn('posts', response.context)
