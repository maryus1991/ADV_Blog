from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from mail_templated import EmailMessage
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, GenericAPIView

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.crypto import get_random_string
from django.urls import reverse
import datetime

from django.conf import settings
from utils.SendEmailThread import SendEmailThread
from accounts.models import User

from .serializers import (
    UserSerializer,
    CustomAuthTokenSerializer,
    CustomJWTTokenObtainPairViewSerializer,
    ChangePasswordSerializer,
    ChangeEmailSerializer,
    ChangeUserInformation,
)

from .permissions import NotAuthenticatedPermissions, IsOwner

# ===================== Registration ==========================


class Registrations(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [NotAuthenticatedPermissions]

    def post(self, request, *args, **kwargs):
        # set post method for creation
        # serialize the data with serializer
        serializer = self.serializer_class(data=request.data)

        # validate the serializer data
        serializer.is_valid(raise_exception=True)

        # get the email and check the email is exist
        email = serializer.validated_data.get("email")
        user_exist = User.objects.filter(email=email).exists()

        # check with if statement
        if not user_exist:

            # create the user
            serializer.save()

            # get the user again and set the verify code
            user = User.objects.filter(email=email).first()

            user.verified_code = get_random_string(255)
            user.save

            # set the context for send it to email template
            context = {
                "url": str(request.get_host())
                + reverse("ConformAccount", kwargs={"token": user.verified_code})
            }

            # create email object
            email_message = EmailMessage(
                "Email/ActivationAccount.tpl",
                context,
                settings.EMAIL_HOST_USER,
                [user.email],
            )

            # send email with threading
            SendEmailThread(email_message).start()

            return Response(
                f""" your account has been created successfully and send conform code for this email ({email}) please conform and verify your email to login """,
                status=status.HTTP_201_CREATED,
            )

        else:

            # raise validation error if email is exist
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


# ================= Token Authentications =====================


class CustomAuthenticationsToken(ObtainAuthToken):
    # custom ObtainAuthToken for custom user model

    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        # post method for create and showing token for every user

        # get the serializer and validate the data
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        # getting the user
        user = serializer.validated_data.get("user")

        # create token object
        token, created = Token.objects.get_or_create(user=user)

        # return the response
        return Response(
            {"token": token.key, "email": user.email}, status=status.HTTP_200_OK
        )


class CustomLogoutToken(APIView):
    """
    for log out the user and delete the token
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # for delete the token object and return not content Response
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ====================== JWT ==================================


class CustomTokenObtainPairView(TokenObtainPairView):
    # set the custom serializer for  TokenObtainPairView

    serializer_class = CustomJWTTokenObtainPairViewSerializer


# ================== edit profile =============================


class UserInformationShowing(RetrieveAPIView):
    """
    for get user information
    """

    permission_classes = [IsOwner]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserChangePassWord(UpdateAPIView):
    """
    create api view for change pass
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    http_method_names = ["put"]

    def get_queryset(self):
        # get and overwrite the query set for selecting only one user
        uid = self.kwargs.get("pk")
        return User.objects.filter(id=uid)

    def update(self, request, *args, **kwargs):
        # custom get the data and update
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # get the email and passwords
        email = request.user.email
        current_password = serializer.validated_data.get("password")
        new_password = serializer.validated_data.get("new_password")

        # get the user id
        uid = kwargs.get("pk")

        # get the user by id and email
        user = User.objects.filter(id=uid, email=email).first()

        # check if the user is exist
        if user is not None:

            # check if user is active and verify
            if user.is_active and user.is_verified:

                # checking user current password
                if user.check_password(current_password):

                    # set new password for user
                    user.set_password(new_password)
                    return Response(
                        "your password is successfully change",
                        status=status.HTTP_202_ACCEPTED,
                    )

                else:
                    # set error for wrong pass
                    return Response(
                        "user wrong information", status=status.HTTP_406_NOT_ACCEPTABLE
                    )

            else:
                # set activations error
                return Response("user not active", status=status.HTTP_401_UNAUTHORIZED)

        else:
            # set error for user not found
            return Response("user not found", status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_202_ACCEPTED)


class UserChangeEmail(UpdateAPIView):
    """
    changing user email
    """

    serializer_class = ChangeEmailSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["put"]

    def get_queryset(self):
        # get and overwrite the query set for selecting only one user
        uid = self.kwargs.get("pk")
        return User.objects.filter(id=uid)

    def update(self, request, *args, **kwargs):
        """
        change user email
        """

        # get and validate serializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # get email
        email = serializer.validated_data.get("email")

        # get user pk and get user object
        uid = kwargs.get("pk")
        user = User.objects.filter(id=uid, email=request.user.email)

        # check user is exist
        if user.exists():

            # get the if exist
            user = user.first()

            # check if the comming email and current email are same
            if user.email == email:
                return Response(
                    "your email are same", status=status.HTTP_406_NOT_ACCEPTABLE
                )

            # save the new info
            user.email = email
            user.is_verified = False
            user.updated_at = datetime.datetime.now()
            user.verified_code = get_random_string(255)
            user.save()

            # set the context for send it to email template
            context = {
                "url": str(request.get_host())
                + reverse("ConformAccount", kwargs={"token": user.verified_code})
            }

            # create email object
            email_message = EmailMessage(
                "Email/ActivationAccount.tpl",
                context,
                settings.EMAIL_HOST_USER,
                [user.email],
            )

            # send email with threading
            SendEmailThread(email_message).start()

            return Response(
                "your email has been changed successfully please conform it",
                status=status.HTTP_200_OK,
            )

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserChangeProfile(UpdateAPIView):

    # set user change profile or account info
    serializer_class = ChangeUserInformation
    permission_classes = [IsOwner]
    http_method_names = ["put"]

    def update(self, request, *args, **kwargs):
        # update the user information
        # get the serializer and validate it
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # get the user id and email
        # get the email from request
        # and check the user is log in or not
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        email = request.user.email
        uid = kwargs.get("pk")

        # get the user
        user = User.objects.filter(id=uid, email=email)

        # check if user is exist
        if user.exists():

            # get the exist if user is exist
            user = user.first()

            # check if user is active
            if user.is_active and user.is_verified and uid == user.id:

                # update the user

                user.first_name = serializer.validated_data.get("first_name")
                user.last_name = serializer.validated_data.get("last_name")
                user.avatar = serializer.validated_data.get("avatar")
                user.updated_at = datetime.datetime.now()
                user.save()

                return Response(
                    self.serializer_class(user).data, status=status.HTTP_202_ACCEPTED
                )

            else:
                # set error
                return Response(
                    " please verify and active your account",
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

        else:
            # set error
            return Response(" user not found", status=status.HTTP_404_NOT_FOUND)


class AuthenticatedUserInformation(APIView):
    """
    for get and showing the log in user information
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # showing the information with get method
        # get the user id and return it

        user_id = request.user.id
        return Response({"user_id": user_id}, status=status.HTTP_202_ACCEPTED)


# ==================== forgot password ========================


class ForgotPassword(GenericAPIView):
    # create forgot password just for send email

    serializer_class = ChangeEmailSerializer

    def post(self, request, *args, **kwargs):
        # check if the user is log int or not
        if request.user.is_authenticated:
            return Response(
                "your cant user this service while your log in ",
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        # get the serializer and validate it
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # get the email and check it
        email = serializer.validated_data.get("email")
        user_object = User.objects.filter(email=email)

        # check if the email exist
        if user_object.exists():

            # get the exist user
            user = user_object.first()

            # change the verified_code and resent it to user
            user.verified_code = get_random_string(255)
            user.save()

            # set the context for send it to email template
            context = {
                "url": str(request.get_host())
                + reverse("ForgotPassword_token", kwargs={"token": user.verified_code})
            }

            # create email object
            email_message = EmailMessage(
                "Email/ActivationAccount.tpl",
                context,
                settings.EMAIL_HOST_USER,
                [user.email],
            )

            # send email with threading
            SendEmailThread(email_message).start()

            return Response(
                f"an email has been successfully to ({email}) please enter and change your password"
            )
        else:
            # set not found error
            return Response(status=status.HTTP_404_NOT_FOUND)


# =================== account activation ======================


class ActivationAccount(GenericAPIView):
    # create forgot password just for send email

    serializer_class = ChangeEmailSerializer

    def post(self, request, *args, **kwargs):
        # check if the user is log int or not
        if request.user.is_authenticated:
            return Response(
                "your cant user this service while your log in ",
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        # get the serializer and validate it
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # get the email and check it
        email = serializer.validated_data.get("email")
        user_object = User.objects.filter(email=email)

        # check if the email exist
        if user_object.exists():

            # get the exist user
            user = user_object.first()

            # change the verified_code and resent it to user
            user.verified_code = get_random_string(255)
            user.save()

            # set the context for send it to email template
            context = {
                "url": str(request.get_host())
                + reverse("ConformAccount", kwargs={"token": user.verified_code})
            }

            # create email object
            email_message = EmailMessage(
                "Email/ActivationAccount.tpl",
                context,
                settings.EMAIL_HOST_USER,
                [user.email],
            )

            # send email with threading
            SendEmailThread(email_message).start()

            return Response(
                f"an email has been successfully to ({email}) please enter and verify your acount"
            )
        else:
            # set not found error
            return Response(status=status.HTTP_404_NOT_FOUND)
