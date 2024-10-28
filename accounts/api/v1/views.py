from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status


from accounts.models import User
from .serializers import UserSerializer
from .permissions import NotAuthenticatedPermissions

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
