from django import forms
from django.urls import reverse

from .fixtures import PostFixturesTest

from ..models import Post, Comment
from ..forms import CommentForm


class PostPagesTests(PostFixturesTest):

    

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
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
            (reverse('posts:create')): 'posts/create_post.html',
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

        check_object = response.context['page_obj'][1]
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
            reverse('posts:create')
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
        last_object = response.context['page_obj'][1]
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
        last_object = response.context['page_obj'][1]
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
            (reverse('posts:index') + '?page=3'): 5,
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

    def test_search_function(self):
        """тест: проверяем работу поиска"""
        response = self.authorized_client.get(
            reverse('posts:search'), {'search': 'Первая'}
        )
        search_object = response.context['posts'][0]
        post_text = search_object.text
        post_author = search_object.author
        post_group = search_object.group

        self.assertEqual(post_text, self.check_objects.text)
        self.assertEqual(post_author, self.check_objects.author)
        self.assertEqual(post_group, self.check_objects.group)

    def test_search_no_results(self):
        """тест: проверяем работу поиска, когда нет результатов"""
        response = self.authorized_client.get(
            reverse('posts:search')
        )
        self.assertEqual(response.context['posts'], None)

    def test_image_in_context(self):
        """Проверяем, что в контекст главной страницы
        передается картинка."""
        response = self.authorized_client.get(
            reverse('posts:index')
        )
        first_object = response.context['page_obj'][0]
        image_field = first_object.image
        self.assertEqual(image_field, self.post.image)

    def test_image_in_group_list(self):
        """Проверяем, что в контекст страницы группы
        передается картинка."""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        )
        first_object = response.context['page_obj'][0]
        image_field = first_object.image
        self.assertEqual(image_field, self.post.image)

    def test_image_in_profile(self):
        """Проверяем, что в контекст страницы профиля
        передается картинка."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user})
        )
        first_object = response.context['page_obj'][0]
        image_field = first_object.image
        self.assertEqual(image_field, self.post.image)

    def test_image_in_post_detail(self):
        """Проверяем, что в контекст страницы поста
        передается картинка."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        first_object = response.context['post']
        image_field = first_object.image
        self.assertEqual(image_field, self.post.image)

    def test_comment_form_in_context(self):
        """В контекст страницы поста передается форма комментария."""
        post = Post.objects.create(text='Тестовый пост', author=self.user)
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': post.id})
        )
        form = response.context.get('comment_form')
        self.assertIsInstance(form, CommentForm)

    def test_comment_appears_in_post_detail(self):
        """Созданный комментарий появляется на странице поста."""
        post = Post.objects.create(text='Пост с комментом', author=self.user)
        comment = Comment.objects.create(post=post, author=self.user, text='Комментарий')
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': post.id})
        )
        comments = response.context['comment_list']
        self.assertIn(comment, comments)

    def test_comment_not_in_other_post(self):
        """Комментарий не появляется в другом посте."""
        post1 = Post.objects.create(text='Пост 1', author=self.user)
        post2 = Post.objects.create(text='Пост 2', author=self.user)
        comment = Comment.objects.create(post=post1, author=self.user, text='Комментарий')
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': post2.id})
        )
        comments = response.context['comment_list']
        self.assertNotIn(comment, comments)

    def test_guest_cannot_see_comment_form(self):
        """Неавторизованный пользователь не видит форму для добавления комментария."""
        post = Post.objects.create(text='Пост для гостя', author=self.user)
        response = self.guest_client.get(
            reverse('posts:post_detail', kwargs={'post_id': post.id})
        )
        form = response.context.get('comment_form')
        self.assertIsNone(form)

    def test_comment_form_in_context(self):
        """Проверяем, что в контекст страницы поста
        передается форма комментария."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post_with_comment.id})
        )
        form = response.context.get('comment_form')
        self.assertIsInstance(form, CommentForm)

    def test_comment_appears_in_post_detail(self):
        """Проверяем, что созданный комментарий
        появляется на странице поста."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post_with_comment.id})
        )
        comments = response.context['comment_list']
        self.assertIn(self.comment, comments)

    def test_comment_not_in_other_post(self):
        """Проверяем, что комментарий не появляется
        в другом посте."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        comments = response.context['comment_list']
        self.assertNotIn(self.comment, comments)

    def test_guest_cannot_see_comment_form(self):
        """Проверяем, что неавторизованный пользователь
        не видит форму для добавления комментария."""
        response = self.guest_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post_with_comment.id})
        )
        form = response.context.get('comment_form')
        self.assertIsNone(form)

    def test_authorized_user_can_add_comment(self):
        self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.id}),
            {'text': 'Новый комментарий'},
            follow=True
        )
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        self.assertContains(response, 'Новый комментарий')

    def test_empty_comment_not_added(self):
        self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.id}),
            {'text': ''},
            follow=True
        )
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        self.assertNotContains(response, '<div class="media-body">')

    def test_guest_cannot_add_comment(self):
        response = self.guest_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.id}),
            {'text': 'Гостевой комментарий'},
            follow=True
        )
        self.assertRedirects(response, f'/auth/login/?next=/posts/{self.post.id}/comment')