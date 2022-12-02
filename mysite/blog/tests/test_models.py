from django.test import TestCase
from blog.tests.test_model_mixin_testcase import ModelMixinTestCase
from blog.models import Post


class PostModelTest(ModelMixinTestCase, TestCase):
    def test_published_manager_only_returns_published_posts(self):
        published_posts = Post.published.get_queryset()
        posts_with_status_published = Post.objects.filter(status="published")

        self.assertQuerysetEqual(
            published_posts,
            posts_with_status_published,
        )
