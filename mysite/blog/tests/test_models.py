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

    def test_get_top_four_similar_posts_returns_empty_for_post_without_tag(
        self,
    ):
        self.assertQuerysetEqual(
            Post.objects.none(),
            self.published_post.get_top_four_similar_posts(),
        )

    def test_get_top_four_similar_posts_returns_similar_posts_for_post_with_tag(
        self,
    ):

        posts = self.create_published_posts(count=2)
        first_post = posts[0]
        first_post.tags.add("test")
        second_post = posts[1]
        second_post.tags.add("test")

        self.assertTrue(second_post in first_post.get_top_four_similar_posts())
