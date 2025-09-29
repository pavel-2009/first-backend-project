from django.test import TestCase, Client


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_static_urls(self):
        """Проверка доступности адресов."""
        urls_status_code = {
            '/about/author/': 200,
            '/about/tech/': 200
        }
        for url, status_code in urls_status_code.items():
            with self.subTest(urls=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, status_code)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'about/author.html': '/about/author/',
            'about/tech.html': '/about/tech/',
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)
