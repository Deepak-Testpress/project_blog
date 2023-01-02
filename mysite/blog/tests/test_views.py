from django.test import TestCase
from django.urls import reverse
from blog.models import Post
from blog.tests.test_model_mixin_testcase import ModelMixinTestCase


class TestViews(ModelMixinTestCase, TestCase):
    def test_post_list_template(self):
        post_list_url = reverse("blog:post_list")
        response = self.client.get(post_list_url)

        self.assertTemplateUsed(response, "blog/post/list.html")

    def test_post_detail_template(self):
        post_detail_url = reverse(
            "blog:post_detail",
            kwargs={
                "year": self.published_post.publish.year,
                "month": self.published_post.publish.month,
                "day": self.published_post.publish.day,
                "post_slug": self.published_post.slug,
            },
        )
        response = self.client.get(post_detail_url)

        self.assertTemplateUsed(response, "blog/post/detail.html")

    def test_post_detail_returns_404_for_invalid_post(self):
        post_detail_url = reverse(
            "blog:post_detail",
            kwargs={
                "year": 2097,
                "month": 12,
                "day": 12,
                "post_slug": "slug-that-does-not-exist",
            },
        )
        response = self.client.get(post_detail_url)

        self.assertEqual(404, response.status_code)

    def test_pagination_returns_404_if_page_out_of_range(self):
        invalid_page_number = 999
        response = self.client.get(
            reverse("blog:post_list"),
            {
                "page": invalid_page_number,
                "posts": self.create_published_posts(4),
            },
        )
        self.assertEquals(404, response.status_code)

    def test_pagination_returns_first_page_if_page_is_empty(self):
        response = self.client.get(
            reverse("blog:post_list"),
            {"page": "", "posts": self.create_published_posts(4)},
        )
        self.assertEquals(1, response.context["page"].number)

    def test_pagination_returns_404_if_string_is_passed_in_page(self):
        response = self.client.get(
            reverse("blog:post_list"),
            {"page": "test", "posts": self.create_published_posts(4)},
        )
        self.assertEquals(404, response.status_code)
