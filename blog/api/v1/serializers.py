from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from django.urls import reverse

from blog.models import Post, PostsComment

User = get_user_model()


class UserModelSerializer(serializers.ModelSerializer):
    """
    create user serializer for  posts author
    """

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "avatar")


class PostsCommentModelSerializer(serializers.ModelSerializer):
    """
    comment model serializer
    """

    class Meta:
        model = PostsComment
        exclude = ["is_active"]
        read_only_fields = ["id", "post"]


class PostModelSerializer(serializers.ModelSerializer):
    """
    create serializer for posts model
    """

    # set author from user model serializer
    author = UserModelSerializer(read_only=True)

    class Meta:
        model = Post
        exclude = ["is_active"]
        read_only_fields = ["id", "author"]

    def to_representation(self, instance):
        """
        for edit and set post url and set the comment for the post
        """
        # get the request and representation
        request = self.context.get("request")
        representation = super().to_representation(instance)

        # if the user see the retrieve object
        if request.parser_context.get("kwargs").get("pk"):

            # declare comment_dict and get parent_comments that there parent is None
            comment_list = []
            parent_comments = (
                PostsComment.objects.filter(post_id=instance.id, parent=None)
                .prefetch_related("child")
                .order_by("-created_at")
                .all()
            )

            # for set the sub comment with there parent
            for comment in parent_comments:

                # get the serialized data of comment
                result = PostsCommentModelSerializer(
                    comment, context={"request": request}
                ).data

                # set the child of comment with child section in parent comment
                # the result most be like this
                #   {
                #   ...
                #   parent comment
                #   ...
                #   child:[
                # ...
                #       sub comments
                # ...
                #   ]
                #  }

                # set the the serialize data  of sub_comment at child field of parent comment  and set the result in comment_list
                result["child"] = [
                    PostsCommentModelSerializer(
                        sub_comment, context={"request": request}
                    ).data
                    for sub_comment in comment.child.all()
                ]
                comment_list.append(result)

            # send the serialized data of comments with representation
            representation["comments"] = comment_list
        else:
            # if user see the list view he will got the post link for see the detail of the post
            representation["post_link"] = reverse(
                "post-detail", kwargs={"pk": instance.id}
            )

        return representation

    def create(self, validated_data):
        # for create a post should be staff user
        # get request and check user is staff or raise error

        request = self.context.get("request")

        if request.user.is_active and request.user.is_verified:

            validated_data["author"] = self.context.get("request").user
            return super().create(validated_data)

        else:
            raise AuthenticationFailed(
                "Not Allowed to create posts please verify and active your account"
            )

    def update(self, instance, validated_data):
        # for update a post should be staff user
        # get request and check user is staff or raise error

        request = self.context.get("request")

        if request.user.is_active and request.user.is_verified:

            # check if the user id staff and owner of th post to change it
            if instance.author.email == self.context.get("request").user.email:
                validated_data["author"] = self.context.get("request").user
                return super().update(instance, validated_data)
            else:
                raise AuthenticationFailed("Not Allowed to update an created posts")
        else:
            raise AuthenticationFailed("Not Allowed to update posts")
