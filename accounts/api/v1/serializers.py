from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password


from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
        fields = [
            "email",
            "first_name",
            "last_name",
            "avatar",
            "password",
            "conform_password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        # set validate password for checking the password and conform password

        # checking the the passwords is same
        if attrs.get("password") != attrs.get("conform_password"):
            raise serializers.ValidationError(
                {"details": "your passwords does not match"}
            )

        # checking the validate password
        try:
            validate_password(attrs.get("password"))

        except ValidationError as error:
            raise serializers.ValidationError({"password": list(error.messages)})

        return super().validate(attrs)

    def create(self, validated_data):
        # overwrite the create method
        # use create user method for more safety

        user = User.objects.create_user(
            email=validated_data.get("email"), password=validated_data.get("password")
        )

        # set other fields
        user.first_name = validated_data.get("first_name")
        user.last_name = validated_data.get("last_name")
        user.avatar = validated_data.get("avatar")
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
        trim_whitespace=True,
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
        if not user.is_active:
            raise serializers.ValidationError(
                {"details": "please verified or activate your account"}
            )

        # checking the user password
        if not user.check_password(password):
            raise serializers.ValidationError({"details": "your password is incorrect"})

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


# ===================== JWT =============================


class CustomJWTTokenObtainPairViewSerializer(TokenObtainPairSerializer):
    """
    create custom TokenObtainPairSerializer for simple jwt for
    check the user verify and activations account
    """

    def validate(self, attrs):
        # validate the user info
        validated_data = super().validate(attrs)

        # for send the email and showing it with tokens
        validated_data["email"] = self.user.email
        validated_data["uid"] = self.user.id

        # get the user
        user = self.user

        # check if the user is active and verify his account
        if user.is_active:
            return validated_data

        # raise error if the user not active and now verify his account
        raise serializers.ValidationError(
            {"details": "please verified or activate your account"}
        )


# ================== edit user account ==================


class ChangePasswordSerializer(serializers.Serializer):

    # create Change pass serializer

    password = serializers.CharField(write_only=True, max_length=255, required=True)
    new_password = serializers.CharField(write_only=True, max_length=255, required=True)
    conform_new_password = serializers.CharField(
        write_only=True, max_length=255, required=True
    )

    def validate(self, attrs):
        # set validate password for checking the password and conform password

        # checking the the passwords is same
        if attrs.get("new_password") != attrs.get("conform_new_password"):
            raise serializers.ValidationError(
                {"details": "your passwords does not match"}
            )

        # checking the validate password
        try:
            validate_password(attrs.get("new_password"))

        except ValidationError as error:
            raise serializers.ValidationError({"new_password": list(error.messages)})

        return super().validate(attrs)


class ChangeEmailSerializer(serializers.Serializer):
    """
    create user  email serializer
    """

    email = serializers.EmailField(required=True)


class ChangeUserInformation(serializers.Serializer):
    """
    create serializer for for last and first name and avatar changing
    """

    first_name = serializers.CharField(trim_whitespace=True, max_length=255)
    last_name = serializers.CharField(trim_whitespace=True, max_length=255)
    avatar = serializers.ImageField(allow_empty_file=True)
