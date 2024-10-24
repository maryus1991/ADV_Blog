from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import filters
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status

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

    # set the serializer class
    serializer_class = PostsCommentModelSerializer

    def get_queryset(self):
        """
        fix the query set to show just the post comments 
        """
        post_id = self.kwargs.get('post_id')
        return PostsComment.objects.filter(post_id=post_id).order_by('-id').all()
    

    def create(self, request, *args, **kwargs):
        """
        overwintering the create method to fixing the error
        """

        # getting the data
        data: dict = request.data
        
        # check the data should not be None
        if data is not None:
            # get the fields
            full_name, email, comment, parent = data.get('full_name'), data.get('email'), data.get('comment'), data.get('parent'),

            # check if the field should not be empty 
            if full_name != '' and email != '' and comment != '':

                # check that the field should not be None
                if full_name is not None and email is not None and comment is not None:
                    
                    # getting the post id
                    post_id = kwargs.get('post_id')
                    

                    # convert the parent to int and return error if can not convert it 
                    try:
                        parent = int(parent)
                    except:
                        return Response('your parent id is not Found able', status=status.HTTP_406_NOT_ACCEPTABLE)


                    # add controller for parent id 
                    if parent == '' or parent == 0 or parent is None :
                        # find and set the None value for parent 
                        parent = None
                    else:
                        # check if the parent is ok 
                        if PostsComment.objects.filter(post_id=post_id, id=parent).first() is None:
                            # set error if parent comment is not find able 
                            return Response('your parent is not find able', status=status.HTTP_406_NOT_ACCEPTABLE)
                        

                    # create the object 
                    PostsComment.objects.create(
                        post_id=post_id,
                        full_name= full_name,
                        email= email,
                        comment= comment,
                        parent_id= parent,
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