from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from django.urls import reverse
import datetime
from blog.models import Post, PostsComment

User = get_user_model()

class UserModelSerializer(serializers.ModelSerializer):
    """
    create user serializer for  posts author
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar')


class PostsCommentModelSerializer(serializers.ModelSerializer):
    """
    comment model serializer 
    """

    class Meta:
        model = PostsComment
        exclude = ['is_active']
        read_only_fields = ['id']



class PostModelSerializer(serializers.ModelSerializer):
    """
    create serializer for posts model 
    """
    # set author from user model serializer
    author = UserModelSerializer(read_only=True)

    class Meta:
        model = Post
        exclude = ['is_active']
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
            comment_dict = {}
            parent_comments =  PostsComment.objects.filter(post_id=instance.id, parent=None).prefetch_related('child').all()

            # serialize the data
            parent_comments = PostsCommentModelSerializer(parent_comments, context={'request': request})

            # for set the sub comment for there parent 
            for comment in parent_comments:
                comment_dict[comment] = [sub_comment for sub_comment in comment.child.all()]

            # send the serialized data of comments with representation
            representation['comments'] = comment_dict
        else:
            # if user see the list view he will got the post link for see the detail of the post
            representation['post_link'] = reverse('post-detail', kwargs={'pk': instance.id})
            

        return representation
    
    def create(self, validated_data):

        # for create a post should be staff user 
        # get request and check user is staff or raise error
        if self.context.get('request').user.is_staff:

            validated_data['author'] = self.context.get('request').user
            return super().create(validated_data)
        else:
            raise AuthenticationFailed('Not Allowed to create posts')
        
    def update(self, instance, validated_data):
        # for update a post should be staff user 
        # get request and check user is staff or raise error

        if self.context.get('request').user.is_staff:

            # check if the user id staff and owner of th post to change it 
            if instance.author.email == self.context.get('request').user.email :

                validated_data['author'] = self.context.get('request').user
                return super().update(instance, validated_data)
            else:
                raise AuthenticationFailed('Not Allowed to update an created posts')
        else:
            raise AuthenticationFailed('Not Allowed to update posts')



    