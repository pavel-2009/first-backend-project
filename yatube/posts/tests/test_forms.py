from django import forms, test

from posts.models import Post, Group, User
from posts.forms import PostForm
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
        self.assertTrue(Post.objects.filter(text='New post text', group=self.group).exists())

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