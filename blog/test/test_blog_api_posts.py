from django.urls import reverse
from rest_framework.test import APIClient

import pytest

from accounts.models import User
from blog.models import Post, PostsComment, PostViews


user_options = {
    "email": "admin@admin.domain",
    "password": "@Aa1234567890",
}


@pytest.fixture
def client():

    # create user
    user = User.objects.create_user(
        email=user_options.get("email"), password=user_options.get("password")
    )

    user.is_verified = True
    user.is_active = True

    user.save()

    # create anonymous and logged in request

    anonymous_client = APIClient()

    client = APIClient()

    # get jwt token and check
    jwt_url = reverse("CustomTokenObtainPairView_API")

    result = client.post(jwt_url, user_options)
    assert result.status_code == 200

    jwt_token = result.json().get("access")

    # set the header
    headers = {"HTTP_AUTHORIZATION": "Bearer " + jwt_token}
    client.credentials(**headers)

    """
    the return is about three section in tuple the first is the jwt token in header client the second is the response for getting
    jwt tokens and the third is for sending anonymous requests and for forth option is user
    """

    return (client, anonymous_client, result.json(), user)


@pytest.mark.django_db
class TestPostsApi:

    def test_create_post_and_create_comment_api_with_valid_data(self, client):

        # get the urls
        create_post_url = reverse("post-list")

        # send request
        response = client[0].post(
            create_post_url,
            {
                "author_id": client[-1].id,
                "title": "test",
                "text": "test",
                "text2": "test",
            },
        )

        # check the status code and db for this post
        assert response.status_code == 201

        # get the post object
        post = Post.objects.filter(author_id=client[-1].id, title="test", text="test")
        assert post.exists() == True

        # get create comment url and send request
        create_comment_url = reverse(
            "comment-list", kwargs={"post_id": post.first().id}
        )
        response = client[1].post(
            create_comment_url,
            {
                "full_name": "mez",
                "email": "user@example.com",
                "comment": "test",
            },
        )

        # check the status code and db
        assert response.status_code == 201
        comment = PostsComment.objects.filter(full_name="mez", email="user@example.com")
        assert comment.exists() == True

        # check the post and comment post
        assert comment.first().post.id == post.first().id

    def test_get_and_retrieve_posts_and_count_views_and_get_and_retrieve_comments_api(
        self, client
    ):

        # get or create a post and comment
        post = Post.objects.get_or_create(
            author_id=client[-1].id,
            title="test",
            text="test",
            text2="test",
        )[0]

        PostsComment.objects.create(
            post=post, full_name="mez", email=user_options.get("email"), comment="test"
        )

        # get urls and send request and check status code
        get_all_posts_url = reverse("post-list")
        retrieve_post_url = reverse("post-detail", kwargs={"pk": post.pk})

        get_all_comment_of_post_url = reverse(
            "comment-list", kwargs={"post_id": post.pk}
        )

        # retrieve_comment_of_post_url = reverse(
        #     "comment-detail",
        #     kwargs={"post_id": post.pk, "pk": post.postscomment_set.first().id},
        # )

        assert client[1].get(get_all_posts_url).status_code == 200
        assert client[1].get(retrieve_post_url).status_code == 200
        assert client[1].get(get_all_comment_of_post_url).status_code == 200
        assert client[1].get(retrieve_post_url).status_code == 200

        # get view objects for test
        visit_counter_second_objects = PostViews.objects.filter(post=post).first()
        assert visit_counter_second_objects.count > 0
        assert visit_counter_second_objects.ip is not None

    def test_update_posts_and_comment_with_valid_data_and_with_put_method(self, client):

        # get post object and comment
        post = Post.objects.create(author_id=client[-1].id, title="test", text="test")
        comment = PostsComment.objects.create(
            post_id=post.id,
            email=user_options.get("email"),
            comment="test",
            full_name="mez",
        )

        # get the urls
        post_update_url = reverse("post-detail", kwargs={"pk": post.pk})
        comment_update_url = reverse(
            "comment-detail", kwargs={"pk": comment.pk, "post_id": post.pk}
        )

        # send put request to update
        response_post = client[0].put(
            post_update_url,
            {
                "title": "11234",
                "text": "1234",
                "text2": "123444",
            },
        )

        response_comment = client[0].put(
            comment_update_url,
            {
                "full_name": "mostafa",
                "comment": "123456788",
                "email": user_options.get("email"),
            },
        )

        # check the status code

        assert response_post.status_code == 200
        assert response_comment.status_code == 202

        # check the data base

        # get post  updated object and comment
        update_post_object = Post.objects.filter(id=post.id).first()
        update_comment_object = PostsComment.objects.filter(id=comment.id).first()

        # check the objects
        assert post.title != update_post_object.title
        assert post.text != update_post_object.text
        assert post.text2 != update_post_object.text2
        assert comment.full_name != update_comment_object.full_name
        assert comment.comment != update_comment_object.comment

    def test_update_posts_and_comment_with_valid_data_and_with_patch_method(
        self, client
    ):
        # get post object and comment
        post = Post.objects.create(author_id=client[-1].id, title="test", text="test")
        comment = PostsComment.objects.create(
            post_id=post.id,
            email=user_options.get("email"),
            comment="test",
            full_name="mez",
        )

        # get the urls
        post_update_url = reverse("post-detail", kwargs={"pk": post.pk})
        comment_update_url = reverse(
            "comment-detail", kwargs={"pk": comment.pk, "post_id": post.pk}
        )

        # send put request to update
        response_post = client[0].patch(
            post_update_url,
            {
                "title": "11234",
                "text2": "123444",
            },
        )

        response_comment = client[0].patch(
            comment_update_url,
            {
                "full_name": "mostafa",
                "comment": "123456788",
            },
        )

        # check the status code

        assert response_post.status_code == 200
        assert response_comment.status_code == 202

        # check the data base

        # get post  updated object and comment
        update_post_object = Post.objects.filter(id=post.id).first()
        update_comment_object = PostsComment.objects.filter(id=comment.id).first()

        # check the objects
        assert post.title != update_post_object.title
        assert post.text == update_post_object.text
        assert post.text2 != update_post_object.text2
        assert comment.full_name != update_comment_object.full_name
        assert comment.comment != update_comment_object.comment

    def test_delete_posts_and_comments_status_code_204(self, client):

        # get post object and comment
        post = Post.objects.create(author_id=client[-1].id, title="test", text="test")
        comment = PostsComment.objects.create(
            post_id=post.id,
            email=user_options.get("email"),
            comment="test",
            full_name="mez",
        )
        assert post.id == comment.post.id

        # get the urls
        post_update_url = reverse("post-detail", kwargs={"pk": post.pk})
        comment_update_url = reverse(
            "comment-detail", kwargs={"pk": comment.pk, "post_id": post.pk}
        )

        # send the requests
        post_update_response = client[0].delete(post_update_url)
        comment_update_response = client[0].delete(comment_update_url)

        # check the status

        assert post_update_response.status_code == 204
        assert comment_update_response.status_code == 204

        # check the data base
        # get post object and comment if exist
        post = Post.objects.filter(id=post.id).first()
        comment = PostsComment.objects.filter(id=comment.pk).exists()

        # check the object
        assert post.is_active == False
        assert comment == False
