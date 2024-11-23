from django.test import TestCase
from django.contrib.auth import get_user_model

from blog.models import Category, PostsComment, Post, PostViews

User = get_user_model()


class TestPostCategoryPostViewsCommentsModels(TestCase):
    """
    test the blog models
    """

    def setUp(self):
        # create user as author
        user = User.objects.create_user(email="post@post.com", password="1234")

        user.is_verified = True
        user.save()

        # create a post and test it here
        post = Post.objects.create(title="test", author=user, text="test")

        # get the post and check
        post = Post.objects.filter(title="test", id=post.id).exists()
        self.assertTrue(post)

    def test_category_model_and_post_model_with_valid_data(self):
        # create category object
        category = Category.objects.create(
            title="test",
            slug="test",
        )

        # create post object
        post = Post.objects.get(title="test")
        post.category = category
        post.save()

        # get the objects again
        category = Category.objects.get(slug="test")

        post = Post.objects.get(title="test")

        # check the objects
        self.assertEqual(post.category, category)

    def test_post_view_model_with_valid_data(self):

        # get the post object
        post = Post.objects.get(title="test")

        # create view object
        view = PostViews.objects.create(
            post=post,
            ip="test",
        )

        # check the view object ang get if again
        view = PostViews.objects.get(ip="test")
        self.assertEqual(view.user, None)
        self.assertEqual(view.count, 0)
        self.assertEqual(view.post, post)

    def test_comment_model_with_valid_data(self):

        # get the post object
        post = Post.objects.get(title="test")

        # create comment object
        comment = PostsComment.objects.create(
            full_name="mez",
            email="test@test.com",
            comment="test",
            post=post,
        )
        sub_comment = PostsComment.objects.create(
            full_name="mez",
            email="test@test.com",
            comment="test",
            post=post,
            parent=comment,
        )

        # get the objects again
        comment = PostsComment.objects.get(id=comment.id)
        sub_comment = PostsComment.objects.get(id=sub_comment.id)
        post = Post.objects.get(title="test")

        # check comments and there subs
        self.assertEqual(comment.child.first().id, sub_comment.id)
        self.assertEqual(post.postscomment_set.last().id, comment.id)
        self.assertEqual(post.postscomment_set.last().child.first().id, sub_comment.id)
