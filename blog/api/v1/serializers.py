from django.contrib import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from blog.models import Post

User = get_user_model()

class UserModelSerializer(serializers.Serializer):
    """
    create user serializer for  posts author
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar')


class PostModelSerializer(serializers.Serializer):
    """
    create serializer for posts model 
    """
    # set author from user model serializer
    author = UserModelSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '*'
    
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
            validated_data['author'] = self.context.get('request').user
            return super().update(instance, validated_data)
        else:
            raise AuthenticationFailed('Not Allowed to create posts')
