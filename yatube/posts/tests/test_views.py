from django import test
from django.urls import reverse
from django import forms

from posts import views
from posts.models import Post, Group, User

class PostPagesTests(test.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser')

        cls.group = Group.objects.create(
            title='Test Group',
            slug='test-group',
            description='A test group'
        )
        
        for i in range(15):
            Post.objects.create(
                author=cls.user,
                text=f'Test Post {i}',
                group=cls.group
            )

        cls.post = Post.objects.create(
            author=cls.user,
            text='Test Post',
            group=cls.group
        )
        

    def setUp(self):
        self.guest_client = test.Client()

        self.authorized_client = test.Client()
        self.authorized_client.force_login(self.user)

    def test_views_use_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': self.group.slug}): 'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': self.user.username}): 'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}): 'posts/create_post.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)


    def test_index_page_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        post_group_0 = first_object.group.title
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(post_author_0, self.post.author.username)
        self.assertEqual(post_group_0, self.post.group.title)

    def test_index_page_paginator(self):
        """Проверка паджинатора на главной странице."""
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

        response = self.authorized_client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 6) 

    def test_group_list_page_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        )
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        post_group_0 = first_object.group.title
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(post_author_0, self.post.author.username)
        self.assertEqual(post_group_0, self.post.group.title)

    def test_group_list_page_paginator(self):
        """Проверка паджинатора на странице группы."""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        )
        self.assertEqual(len(response.context['page_obj']), 10)

        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug}) + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), 6)

    def test_profile_page_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username})
        )
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        post_group_0 = first_object.group.title
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(post_author_0, self.post.author.username)
        self.assertEqual(post_group_0, self.post.group.title)

    def test_profile_page_paginator(self):
        """Проверка паджинатора на странице профиля."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username})
        )
        self.assertEqual(len(response.context['page_obj']), 10)

        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username}) + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), 6)

    def test_post_detail_page_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        post = response.context['post']
        self.assertEqual(post, self.post)

    def test_post_create_page_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_edit_page_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id})
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_create_with_group(self):
        """Проверка создания поста с группой."""
        group = Group.objects.create(
            title='New Test Group',
            slug='new-test-group',
            description='A new test group'
        )
        form_data = {
            'text': 'A new post with group',
            'group': group.id
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:profile', kwargs={'username':self.user.username}))
        self.assertTrue(
            Post.objects.filter(
                text='A new post with group',
                group=group,
                author=self.user
            ).exists()
        )

        responce_to_index = self.authorized_client.get(reverse('posts:index'))
        self.assertIn(
            Post.objects.get(text='A new post with group'),
            responce_to_index.context['page_obj'].object_list
        )

        response_to_group = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': group.slug})    
        )
        self.assertIn(
            Post.objects.get(text='A new post with group'),
            response_to_group.context['page_obj'].object_list
        )

        response_to_profile = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username})
        )
        self.assertIn(  
            Post.objects.get(text='A new post with group'),
            response_to_profile.context['page_obj'].object_list
        )