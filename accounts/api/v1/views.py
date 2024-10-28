from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated


from accounts.models import User
from .serializers import UserSerializer, CustomAuthTokenSerializer
from .permissions import NotAuthenticatedPermissions

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