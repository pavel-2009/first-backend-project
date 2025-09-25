from django import test

from ..models import Post, Group, User

class PostModelsTest(test.TestCase):
    
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