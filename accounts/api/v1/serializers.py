from rest_framework import serializers
import datetime

from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Create serializer for user 
    and user custom serializer for custom user model 
    """

    # set the conform password for creating user
    conform_password = serializers.CharField(write_only=True, max_length=255)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'avatar', 'password', 'conform_password']

    def validate(self, attrs):
        # set validate password for checking the password and conform password

        # checking the the passwords is same
        if attrs.get("password") != attrs.get("conform_password"):
            raise serializers.ValidationError(
                {"details": "your passwords does not match"}
            )

        # checking the validate password 
        # try:
        #     validate_password(attrs.get("password"))

        # except ValidationError as error:
        #     raise serializers.ValidationError({"password": list(error.messages)})

        return super().validate(attrs)

        
    def create(self, validated_data):
        # overwrite the create method 
        # use create user method for more safety
          
        user = User.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password')
        )

        # set other fields  
        user.first_name = validated_data.get('first_name')
        user.last_name = validated_data.get('last_name')
        user.avatar = validated_data.get('avatar')
        user.save()
        return validated_data