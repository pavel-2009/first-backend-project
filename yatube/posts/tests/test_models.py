from .fixtures import PostFixturesTest


class PostModelTest(PostFixturesTest):
    def test_object_name_is_text_field(self):
        """__str__ post - это срочка с содержимым post.text."""
        post = PostModelTest.post
        expected_object_post = post.text[:15]
        self.assertEqual(expected_object_post, str(post))

    def test_object_name_is_title_field(self):
        """__str__  group - это строчка с содержимым group.title."""
        post = self.post
        expected_object_group = post.group.title
        self.assertEqual(expected_object_group, str(self.group.title))
