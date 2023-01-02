from django.test import TestCase
from blog.models import Post
from django.contrib.auth.models import User


class ModelMixinTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="xezeyan",
            password="xezeyan@password",
        )

        self.draft_post = Post.objects.create(
            title="Test post thats status=draft by default",
            author=self.user,
            body="This post is created by testuser author",
        )
        self.published_post = Post.objects.create(
            title="Test post thats status=published",
            author=self.user,
            body="This post is created by testuser author",
            slug="post-created-testuser-author",
            status="published",
        )

    def create_published_posts(self, count):
        posts = []
        for i in range(count):
            post = Post.objects.create(
                title="Published " + str(i + 1),
                author=self.user,
                body="Testing Published" + str(i + 1),
                status="published",
                slug="published-" + str(i + 1),
            )
            posts.append(post)
        return posts
