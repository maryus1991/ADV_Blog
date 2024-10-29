from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.generics import RetrieveAPIView, UpdateAPIView, GenericAPIView

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView

import datetime

from accounts.models import User

from .serializers import (UserSerializer, 
                            CustomAuthTokenSerializer, 
                            CustomJWTTokenObtainPairViewSerializer, 
                            ChangePasswordSerializer, 
                            ChangeEmailSerializer,
                            ChangeUserInformation)

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
        email = serializer.validated_data.get('email')
        user_exist = User.objects.filter(email=email).exists()

        # check with if statement
        if not user_exist :
            
            # saving the user and send email
            # todo send email
            serializer.save()

            return Response(f'''your account has been created successfully 
                                and send conform code for this email ({email}) 
                                please conform and verify your email to login '''
                                ,status=status.HTTP_201_CREATED
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
            data=request.data,
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)

        # getting the user
        user = serializer.validated_data.get('user')

        # create token object
        token, created = Token.objects.get_or_create(user=user)

        # return the response
        return Response({'token': token.key, 'email': user.email}, status=status.HTTP_200_OK) 


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

    def get_queryset(self):
        # get and overwrite the query set for selecting only one user 
        uid = self.kwargs.get('pk')
        return User.objects.filter(id=uid)
    

    def update(self, request, *args, **kwargs):
        # custom get the data and update 
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # get the email and passwords
        email = request.user.email
        current_password = serializer.validated_data.get('password')
        new_password = serializer.validated_data.get('new_password')

        # get the user id
        uid = kwargs.get('pk')

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
                    return Response('your password is successfully change', status=status.HTTP_202_ACCEPTED)

                else:
                    # set error for wrong pass
                    return Response('user wrong information', status=status.HTTP_406_NOT_ACCEPTABLE)
                
            else:
                # set activations error
                return Response('user not active', status=status.HTTP_401_UNAUTHORIZED)

        else:
            # set error for user not found
            return Response('user not found', status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_202_ACCEPTED)
        

class UserChangeEmail(UpdateAPIView):

    """
    changing user email 
    """

    serializer_class = ChangeEmailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # get and overwrite the query set for selecting only one user 
        uid = self.kwargs.get('pk')
        return User.objects.filter(id=uid)

    def update(self, request, *args, **kwargs):
        """
        change user email 
        """

        # get and validate serializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # get email 
        email = serializer.validated_data.get('email')

        # get user pk and get user object
        uid = kwargs.get('pk')
        user = User.objects.filter(id=uid, email=request.user.email)

        # check user is exist 
        if user.exists():
            # todo send email

            user = user.first()

            # check if the comming email and current email are same
            if user.email == email:
                return Response('your email are same', 
                    status=status.HTTP_406_NOT_ACCEPTABLE)
                

            # save the new info
            user.email = email
            user.is_verified = False
            user.updated_at = datetime.datetime.now()
            user.save()

            return Response('your email has been changed successfully please conform it', 
                    status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserChangeProfile(UpdateAPIView):
    # set user change profile or account info
    serializer_class = ChangeUserInformation
    permission_classes = [IsOwner]

    def update(self, request, *args, **kwargs):
        pass


