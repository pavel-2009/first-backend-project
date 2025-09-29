from django import forms
from django.urls import reverse

from .fixtures import PostFixturesTest


class PostPagesTests(PostFixturesTest):
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            (
                reverse('posts:group_list', kwargs={'slug': 'test-slug'})
            ): 'posts/group_list.html',
            (
                reverse('posts:profile', kwargs={'username': self.user})
            ): 'posts/profile.html',
            (
                reverse('posts:post_detail', kwargs={'post_id': self.post.id})
            ): 'posts/post_detail.html',
            (
                reverse('posts:post_edit', kwargs={'post_id': self.post.id})
            ): 'posts/create_post.html',
            (reverse('posts:post_create')): 'posts/create_post.html',
        }
        # Проверяем, что при обращении к name вызывается соответствующий
        # HTML-шаблон
        for url, template in templates_pages_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_context(self):
        """Проверяем ожидаем контекст"""
        response = self.authorized_client.get(reverse('posts:index'))

        # Взяли рандомный элемент из списка и проверили, что его содержание
        # совпадает с ожидаемым
        check_object = response.context['page_obj'][-1]
        post_text_0 = check_object.text
        post_author_0 = check_object.author

        self.assertEqual(post_text_0, self.check_objects.text)
        self.assertEqual(str(post_author_0), 'auth')

    def test_group_list_correct_context(self):
        """Шаблон group_list - список постов отфильтрованных по группе."""
        response = (self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'test-slug'})
        ))
        group_posts = response.context['page_obj']
        check_object = response.context["page_obj"][0]
        post_text = check_object.text
        post_author = check_object.author
        # проверяем важные дополнительные параметры у постов,
        # имя группы
        self.assertNotIn(self.group, group_posts)
        # проверить количество постов в группе
        self.assertEqual(len(response.context['page_obj']), 10)
        # проверяем любой пост на соответствие
        # по тексту и автору
        self.assertEqual(post_text, self.check_objects.text)
        self.assertEqual(post_author, self.post.author)

    def test_post_profile(self):
        """список постов отфильтрованных по пользователю."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user})
        )
        # проверим, что переданный пользователь, является автором
        # возвращаемых постов
        author = self.user
        self.assertEqual(response.context['author'], author)

    def test_post_details_id(self):
        """posts:posts_details, один пост отфильтрованный по id """
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': 1})
        )
        objects = response.context["post"]
        self.assertEqual(objects.text, self.check_objects.text)

    def test_post_edit_id(self):
        """форма редактированного поста, отфильтраванного по id"""
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': 10})
        )

        form = response.context.get('form')

        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for fields_name, expected in form_fields.items():
            with self.subTest(value=fields_name):
                form_field = form.fields.get(fields_name)
                self.assertIsInstance(form_field, expected)

    def test_create_post_form(self):
        """форма создания поста - что при создание поста,
        создается необходимая поля формы."""
        response = self.authorized_client.get(
            reverse('posts:post_create')
        )

        form = response.context.get('form')

        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for fields_name, expected in form_fields.items():
            with self.subTest(value=fields_name):
                form_field = form.fields.get(fields_name)
                self.assertIsInstance(form_field, expected)

    def test_index_post_show(self):
        """Проверяем что если при создание поста указать группу
         то этот пост появляется на главной странице сайта"""
        response = self.authorized_client.get(
            reverse('posts:index')
        )
        last_object = response.context['page_obj'][-1]
        post_text = last_object.text
        post_author = last_object.author
        post_group = last_object.group

        self.assertEqual(post_text, self.check_objects.text)
        self.assertEqual(post_author, self.check_objects.author)
        self.assertEqual(post_group, self.check_objects.group)

    def test_create_post_with_group(self):
        """проверяет, что если при создание поста, указать групп
        то этот пост появляется на страницы выбранной группы"""
        # Сделать запрос на группы создаваемого поста
        response = self.guest_client.get(
            reverse('posts:group_list', kwargs={'slug': self.post.group.slug})
        )
        expected_object = response.context['page_obj'][0]

        self.assertEqual(
            self.check_objects.group.slug, expected_object.group.slug
        )

    def test_profile_show_correct_context(self):
        """проверяет, что если при создании поста указать группу,
        то этот пост появляется в профайле пользователя."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user})
        )
        last_object = response.context['page_obj'][-1]
        post_text = last_object.text
        post_author = last_object.author
        post_group = last_object.group

        self.assertEqual(post_text, self.check_objects.text)
        self.assertEqual(post_author, self.check_objects.author)
        self.assertEqual(post_group, self.check_objects.group)

    def test_not_in_group(self):
        """проверяем, что пост не попал в группу,
        для которой не был предназначен."""
        response = (self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'test-slug'})
        ))
        objects = response.context['page_obj']
        self.assertNotIn(self.group2, objects)

    def test_pagination(self):
        """тест: проверяем работу паджинатора для разных запросов"""
        urls_paginator_count_post = {
            (reverse('posts:index')): 10,
            (reverse('posts:index') + '?page=2'): 10,
            (reverse('posts:index') + '?page=3'): 4,
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug},
            ): 10,
            (reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug},
            ) + '?page=2'): 5,
            reverse(
                'posts:profile',
                kwargs={'username': self.user}
            ): 10,
            (reverse(
                'posts:profile',
                kwargs={'username': self.user}
            ) + '?page=2'): 10,
            (reverse(
                'posts:profile',
                kwargs={'username': self.user}
            ) + '?page=3'): 4,
        }
        for url, count_post in urls_paginator_count_post.items():
            with self.subTest(value=url):
                response = self.authorized_client.get(url)
                self.assertEqual(len(response.context['page_obj']), count_post)
