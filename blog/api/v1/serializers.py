from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status

import datetime
from blog.models import Post

User = get_user_model()

class UserModelSerializer(serializers.ModelSerializer):
    """
    create user serializer for  posts author
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar')


class PostModelSerializer(serializers.ModelSerializer):
    """
    create serializer for posts model 
    """
    # set author from user model serializer
    author = UserModelSerializer(read_only=True)

    class Meta:
        model = Post
        exclude = ['is_active']
        
    
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



    