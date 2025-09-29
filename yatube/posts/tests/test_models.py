from django.core.exceptions import ValidationError
from django.test import TestCase

from posts.models import Group
from ..models import Post, Group, User

class PostModelsTest(TestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post = Post.objects.create(
            text='Тестовый пост для проверки модели',
            author=User.objects.create_user(username='testuser')
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-group',
            description='Описание тестовой группы'
        )


    def test_post_str(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        expected_str = self.post.text[:15]
        self.assertEqual(expected_str, str(self.post))


    def test_group_str(self):
        """Проверяем, что у модели Group корректно работает __str__."""
        expected_str = self.group.title
        self.assertEqual(expected_str, str(self.group))

    def test_group_verbose_names(self):
        """Проверяем, что у модели Group корректно работает verbose_name."""
        field_verboses = {
            'title': 'Название группы',
            'description': 'Описание группы',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.group._meta.get_field(field).verbose_name, expected_value
                )

    def test_post_verbose_names(self):
        """Проверяем, что у модели Post корректно работает verbose_name."""
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.post._meta.get_field(field).verbose_name, expected_value
                )

    def test_post_help_texts(self):
        """Проверяем, что у модели Post корректно работает help_text."""
        field_help_texts = {
            'text': 'Введите текст поста',
            'group': 'Группа, к которой будет относиться пост',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.post._meta.get_field(field).help_text, expected_value
                )


    def test_group_help_texts(self):
        """Проверяем, что у модели Group корректно работает help_text."""
        field_help_texts = {
            'title': 'Введите название группы',
            'description': 'Введите описание группы',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.group._meta.get_field(field).help_text, expected_value
                )

    def test_meta(self):
        """Проверяем, что у модели Group корректно работает meta."""
        self.assertEqual(self.group._meta.get_field('title').unique, True)
        self.assertEqual(self.group._meta.get_field('title').blank, False)
        self.assertEqual(self.group._meta.get_field('title').null, False)
        self.assertEqual(self.group._meta.get_field('slug').unique, True)
        self.assertEqual(self.group._meta.get_field('slug').blank, False)
        self.assertEqual(self.group._meta.get_field('slug').null, False)




class GroupModelTest(TestCase):
    def test_group_creation_and_str(self):
        group = Group.objects.create(
            title='Тестовая группа',
            slug='test-group',
            description='Описание'
        )
        self.assertEqual(str(group), 'Тестовая группа')

    def test_group_slug_unique(self):
        Group.objects.create(
            title='Группа 1',
            slug='unique-slug',
            description='Описание'
        )
        with self.assertRaises(Exception):
            Group.objects.create(
                title='Группа 2',
                slug='unique-slug',
                description='Другое описание'
            )

    def test_group_required_fields(self):
        group = Group(title='', slug='', description='Описание')
        with self.assertRaises(ValidationError):
            group.full_clean()

    def test_string_representation(self):
        group = Group.objects.create(
            title='Моя группа',
            slug='my-group',
            description='Описание моей группы'
        )
        self.assertEqual(str(group), 'Моя группа')

    def test_help_texts(self):
        group = Group.objects.create(
            title='Группа с подсказками',
            slug='group-with-help',
            description='Описание'
        )
        self.assertEqual(group._meta.get_field('title').help_text, 'Введите название группы')
        self.assertEqual(group._meta.get_field('slug').help_text, 'Введите адрес группы')
        self.assertEqual(group._meta.get_field('description').help_text, 'Введите описание группы')