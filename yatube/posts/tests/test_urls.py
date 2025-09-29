from http import HTTPStatus

from .fixtures import PostFixturesTest


class PostURLTests(PostFixturesTest):
    def test_create(self):
        """Проверка доступа /create/ - только авторизованному пользователю
        create """
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_url_redirect_anonymous(self):
        """create - перенаправляет анонимного пользователя"""
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(
            response, ('/auth/login/?next=/create/')
        )

    def test_edit_author_post(self):
        """ Если пользователя автор поста, то у него есть доступ 200"""
        response = self.authorized_client.get(f'/posts/{self.post.id}/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_not_author_post(self):
        """Если пользователь не автор поста проверка
        переадресация на posts/post_id"""
        response = self.authorized_client_owner.get(
            f'/posts/{self.post.id}/edit/'
        )
        self.assertRedirects(
            response, (
                f'/posts/{self.post.id}/'
            )
        )

    def test_urls_status_code_guest_client(self):
        """Тестирование общедоступных страниц"""
        templates_url_status_code = {
            '/': HTTPStatus.OK,
            f'/group/{self.group.slug}/': HTTPStatus.OK,
            f'/profile/{self.user}/': HTTPStatus.OK,
            f'/posts/{self.post.id}/': HTTPStatus.OK,
            '/unexisting_page/': HTTPStatus.NOT_FOUND,
        }
        for address, status_code in templates_url_status_code.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, status_code)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': "posts/index.html",
            f'/group/{self.group.slug}/': "posts/group_list.html",
            f'/profile/{self.user}/': "posts/profile.html",
            f'/posts/{self.post.id}/': "posts/post_detail.html",
            f'/posts/{self.post.id}/edit/': "posts/create_post.html",
            '/create/': "posts/create_post.html",
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
