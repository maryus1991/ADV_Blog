from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import filters
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from blog.models import Post, PostsComment
import datetime

from .serializers import PostModelSerializer, PostsCommentModelSerializer
from .permissions import IsOwnerOrReadOnly


class PostModelViewSet(ModelViewSet):
    # set model view set for post model
    
    # set the permission class that for post owner user or read only for other users
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class  = PostModelSerializer

    # set filters
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    # set fields for filter and search 
    search_fields = ['title', 'text',  'text2',]
    ordering_fields = ["created_at", 'updated_at']

    # set the query and filter it for is activated posts
    queryset = Post.objects.filter(is_active=True).order_by('-id').all()

    def destroy(self, request, *args, **kwargs):
        """
        delete object if the user ad admin or staff user and his email is the same with author email
        """
        print()
        instance = self.get_object()
        if request.user.is_superuser or ( request.user.is_staff and instance.author.email == request.user.email ):

            # set the object inactivate for not showing again
            instance.is_active = False
            instance.updated_at = datetime.datetime.now()
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise AuthenticationFailed('Your are not allowed to delete ')

class PostCommentModelViewSet(ModelViewSet):
    # permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostsCommentModelSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        print(post_id)
        return PostsComment.objects.filter(post_id=post_id).order_by('-id').all()
    
