from django.test import TestCase
from django.urls import reverse, resolve
from blog.views import PostListView, post_detail, PostShareView
from blog.tests.test_model_mixin_testcase import ModelMixinTestCase


class TestURLs(ModelMixinTestCase, TestCase):
    def test_post_list(self):
        post_list_url = reverse("blog:post_list")
        self.assertEqual(resolve(post_list_url).func.view_class, PostListView)

    def test_post_detail(self):
        post_detail_url = reverse(
            "blog:post_detail",
            kwargs={
                "year": self.published_post.publish.year,
                "month": self.published_post.publish.month,
                "day": self.published_post.publish.day,
                "post_slug": self.published_post.slug,
            },
        )
        self.assertEqual((resolve(post_detail_url).func), post_detail)

    def test_post_share(self):
        self.assertEquals(
            resolve(
                reverse("blog:post_share", args=[self.published_post.id])
            ).func.view_class,
            PostShareView,
        )
