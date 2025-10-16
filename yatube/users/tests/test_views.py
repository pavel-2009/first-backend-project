from django import test
from django.urls import reverse

class UserViewsTests(test.TestCase):
    def setUp(self):
        self.client = test.Client()

    def test_signup_page_uses_correct_template(self):
        """URL-адрес /auth/signup/ использует шаблон users/signup.html."""
        response = self.client.get(reverse('users:signup'))
        self.assertTemplateUsed(response, 'users/signup.html')

    def test_profile_page_uses_correct_template(self):
        """URL-адрес /auth/profile/ использует шаблон users/profile.html."""
        # Создаем и авторизуем пользователя
        self.client.post(reverse('users:signup'), {
            'username': 'testuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        })
        self.client.login(username='testuser', password='complexpassword123')
        
        response = self.client.get(reverse('users:profile'))
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_profile_page_requires_login(self):
        """URL-адрес /auth/profile/ требует авторизации."""
        response = self.client.get(reverse('users:profile'), follow=True)
        self.assertRedirects(response, '/auth/login/?next=/auth/profile/')