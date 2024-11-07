from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status

import datetime

from blog.models import Post, PostsComment, PostViews
from utils.get_ip import get_ip

from .serializers import PostModelSerializer, PostsCommentModelSerializer
from .permissions import IsOwnerOrReadOnly


class PostModelViewSet(ModelViewSet):
    # set model view set for post model

    # set the permission class that for post owner user or read only for other users
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostModelSerializer

    # set filters
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # set fields for filter and search
    search_fields = {
        "title": ['exec', 'in'],
        "text": ['exec', 'in'],
        "text2": ['exec', 'in'],
        'category__title':['in', 'exec'],
        'category__slug':['in', 'exec'],

    }

    filterset_fields = {
        "category": ["exact", "in"],
        "author": ["exact", "in"],
    }

    ordering_fields = ["created_at", "updated_at"]

    # set the query and filter it for is activated posts
    queryset = Post.objects.filter(is_active=True).order_by("-id").all()

    def destroy(self, request, *args, **kwargs):
        """
        delete object if the user ad admin or staff user and his email is the same with author email
        """

        # checking if the user is active and verify his account
        if not request.user.is_verified or not request.user.is_active:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        instance = self.get_object()
        if request.user.is_superuser or (instance.author.email == request.user.email):

            # set the object inactivate for not showing again
            instance.is_active = False
            instance.updated_at = datetime.datetime.now()
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise AuthenticationFailed("Your are not allowed to delete ")
    
    def retrieve(self, request, *args, **kwargs):
        # call and overwrite the retrieve dev for count the views
        
        # getting ip
        ip = get_ip(request)

        # create views is its ip is not exist  or returned it if exist
        view = PostViews.objects.get_or_create(
            post_id=kwargs.get('pk'),
            ip=ip,
            user=request.user if request.user.is_authenticated else None,
        )

        # changing the count of the views
        count = 0
        if view[0].count is not None:
            count = view[0].count

        view[0].count = count + 1
        view[0].save()

        return super().retrieve(request, *args, **kwargs)


class PostCommentModelViewSet(ModelViewSet):

    # set the serializer class
    serializer_class = PostsCommentModelSerializer

    def get_queryset(self):
        """
        fix the query set to show just the post comments
        """
        post_id = self.kwargs.get("post_id")
        return PostsComment.objects.filter(post_id=post_id).order_by("-id").all()

    def create(self, request, *args, **kwargs):
        """
        overwintering the create method to fixing the error
        """

        # getting the data
        data: dict = request.data

        # check the data should not be None
        if data is not None:
            # get the fields
            full_name, email, comment, parent = (
                data.get("full_name"),
                data.get("email"),
                data.get("comment"),
                data.get("parent"),
            )

            # check if the field should not be empty
            if full_name != "" and email != "" and comment != "":

                # check that the field should not be None
                if full_name is not None and email is not None and comment is not None:

                    # getting the post id
                    post_id = kwargs.get("post_id")

                    # convert the parent to int or set null value
                    try:
                        parent = int(parent)
                    except:
                        parent = None

                    # add controller for parent id
                    if parent == "" or parent == 0 or parent is None:
                        # find and set the None value for parent
                        parent = None
                    else:

                        # check if the parent is ok
                        if (
                            PostsComment.objects.filter(
                                post_id=post_id, id=parent
                            ).first()
                            is None
                        ):
                            # set error if parent comment is not find able
                            return Response(
                                "your parent is not find able",
                                status=status.HTTP_406_NOT_ACCEPTABLE,
                            )

                    # create the object
                    PostsComment.objects.create(
                        post_id=post_id,
                        full_name=full_name,
                        email=email,
                        comment=comment,
                        parent_id=parent,
                    )

                    # successfully Create message
                    return Response(status=status.HTTP_201_CREATED)

                else:
                    # setting error for None value
                    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                # setting error for empty string
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            # setting error
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        overwrite update method for fixing the errors
        for edit a comment the user should be login with same comment email
        """

        # set error for noo authorize user
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # get the post id and comment id
        comment_id = kwargs.get("pk")
        post_id = kwargs.get("post_id")

        # get the request data
        data = request.data

        # get the values
        full_name, email, comment = (
            data.get("full_name"),
            data.get("email"),
            data.get("comment"),
        )

        # check if values if not None and not empty string
        if full_name is not None and email is not None and comment is not None:
            if full_name != " " and email != " " and comment != " ":

                # get object from db if exists
                comment = PostsComment.objects.filter(
                    post_id=post_id, id=comment_id
                ).first()

                # check if exist
                if comment is not None:

                    # checking and getting the user
                    user = request.user

                    # check the user
                    if (
                        user is not None
                        and request.user.is_authenticated
                        and user.is_verified
                        and user.is_active
                    ):

                        # check if user email is the same with comment email
                        if user.email == comment.email:

                            # update the object and return 201 status
                            comment.full_name = full_name
                            comment.comment = comment
                            comment.updated_at = datetime.datetime.now()
                            comment.save()

                            return Response(status=status.HTTP_202_ACCEPTED)

                        else:
                            return Response(status=status.HTTP_401_UNAUTHORIZED)

                    else:
                        # set error
                        return Response(status=status.HTTP_401_UNAUTHORIZED)

                else:
                    # not exits error
                    return Response(status=status.HTTP_404_NOT_FOUND)

            else:
                # setting error for empty string
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            # setting error for None value
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        overwriting the destroy method for detaching who can delete the comment
        """

        # set error for noo authorize user
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # get the post id and comment id
        comment_id = kwargs.get("pk")
        post_id = kwargs.get("post_id")

        # get the user
        user = request.user

        # getting and checking the object
        comment = PostsComment.objects.filter(id=comment_id, post_id=post_id).first()

        if comment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        """ checking the user that just the comment owner or admin user can delete the comment  """
        if user.is_superuser or (
            (comment.email == user.email) and user.is_verified and user.is_active
        ):

            # deactivate the objects
            comment.is_active = False
            comment.updated_at = datetime.datetime.now()
            comment.save()

            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
