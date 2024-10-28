from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
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

# ============== token authenticated =====================

class CustomAuthTokenSerializer(serializers.Serializer):
    """
    create custom auth token serializer for changing username field and replaced it with email field as main username field
    """
    # getting the email and password of user
    email = serializers.CharField(label="email", write_only=True)
    password = serializers.CharField(
        label="Password",
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )

    # get the token 
    token = serializers.CharField(label="Token", read_only=True)

    def validate(self, attrs):
        # validate the user
        email = attrs.get("email")
        password = attrs.get("password")
        
        # get the user
        user = User.objects.filter(email=email).first()

        # check if the user is active and verified
        if not user.is_active and not user.is_verified:
            raise serializers.ValidationError(
                {"details": "please verified or activate your account"}
            )

        # checking the user password
        if not user.check_password(password):
            raise serializers.ValidationError(
                {"details": "your password is incorrect"}
            )

        # authenticate the user
        if email and password:
            user = authenticate(
                request=self.context.get("request"),
                email=email,
                password=password,
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
