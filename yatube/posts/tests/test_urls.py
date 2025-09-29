from django import test
from django.urls import reverse

from ..models import Group, Post, User


class PostURLTests(test.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user1 = User.objects.create_user(username='auth')
        cls.user2 = User.objects.create_user(username='noauth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post1 = Post.objects.create(
            author=cls.user1,
            text='Тестовый пост',
            group=cls.group
        )
        cls.post2 = Post.objects.create(
            author=cls.user2,
            text='Тестовый пост 2',
            group=cls.group
        )

    def setUp(self):
        self.guest_client = test.Client()
        self.authorized_client = test.Client()
        self.authorized_client.force_login(self.user1)


    def test_homepage_unauthorised(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_authorised(self):
        response = self.authorized_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_template(self):
        response = self.guest_client.get(reverse('posts:index'))
        self.assertTemplateUsed(response, 'posts/index.html')

    def test_group_list_unauthorised(self):
        response = self.guest_client.get(f'/group/{self.group.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_group_list_authorised(self):
        response = self.authorized_client.get(f'/group/{self.group.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_group_list_template(self):
        response = self.guest_client.get(f'/group/{self.group.slug}/')
        self.assertTemplateUsed(response, 'posts/group_list.html')

    def test_profile_unauthorised(self):
        response = self.guest_client.get(f'/profile/{self.user1.username}/')
        self.assertEqual(response.status_code, 200)

    def test_profile_authorised(self):
        response = self.authorized_client.get(f'/profile/{self.user1.username}/')
        self.assertEqual(response.status_code, 200)

    def test_profile_template(self):
        response = self.authorized_client.get(f'/profile/{self.user1.username}/')
        self.assertTemplateUsed(response, 'posts/profile.html')

    def test_post_detail_unauthorised(self):
        response = self.guest_client.get(f'/posts/{self.post1.id}/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_authorised(self):
        response = self.authorized_client.get(f'/posts/{self.post1.id}/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_template(self):
        response = self.guest_client.get(f'/posts/{self.post1.id}/')
        self.assertTemplateUsed(response, 'posts/post_detail.html')

    def test_create_unauthorised(self):
        response = self.guest_client.get('/create/')
        self.assertRedirects(response, f'/auth/login/?next=/create/')

    def test_create_authorised(self):
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_create_template(self):
        response = self.authorized_client.get('/create/')
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_post_edit_unauthorised(self):
        response = self.guest_client.get(f'/posts/{self.post2.id}/edit/')
        self.assertRedirects(response, f'/auth/login/?next=/posts/{self.post2.id}/edit/')

    def test_post_edit_not_author_authorised(self):
        response = self.authorized_client.get(f'/posts/{self.post2.id}/edit/')
        self.assertRedirects(response, f'/posts/{self.post2.id}/')

    def test_post_edit_author_authorised(self):
        response = self.authorized_client.get(f'/posts/{self.post1.id}/edit/')
        self.assertEqual(response.status_code, 200)

    def test_post_edit_template(self):
        response = self.authorized_client.get(f'/posts/{self.post1.id}/edit/')
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_unexisting_page(self):
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse(
                'posts:group_list', kwargs={'slug': self.group.slug}
            ),
            'posts/profile.html': reverse(
                'posts:profile', kwargs={'username': self.user1.username}
            ),
            'posts/post_detail.html': reverse(
                'posts:post_detail', kwargs={'post_id': self.post1.id}
            ),
            'posts/create_post.html': reverse('posts:post_create'),
            'posts/create_post.html': reverse(
                'posts:post_edit', kwargs={'post_id': self.post1.id}
            ),
        }
        for template, reverse_name in templates_url_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)