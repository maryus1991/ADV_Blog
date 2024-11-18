from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework.test import APIClient
from django.test import TestCase

from accounts.models import User


user_options = {
    "email": "admin@admin.domain",
    "password": "@Aa1234567890",
}



class TestAccountAuthenticatedApi(TestCase):
    
    def setUP(self):

        # create user  
        self.user = User.objects.create_user(
            email = user_options.get('email'),
            password = user_options.get('password')     
        ) 

        self.user.is_verified = True
        self.user.verified_code = get_random_string(255)
        self.user.save()

        # create anonymous and logged in request

        anonymous_client = APIClient()

        client = APIClient()


        # get jwt token and check
        jwt_url = reverse('CustomTokenObtainPairView_API')

        result = client.post(jwt_url, user_options)
        self.assertEqual(result.status_code, 200)

        jwt_token = result.json().get('access') 

        # set the header
        headers = {"HTTP_AUTHORIZATION": "Bearer " + result.json().get("access")}
        client.credentials(**headers)
        


    def test_registration_api_url_with_valid_and_invalid_data(self):

        # get the url
        url = reverse('Registrations_API')

        # send request with valid data
        response = anonymous_client.post(url, {
            "email": "user@example.com",
            "first_name": "mostafa",
            "last_name": "khenifary",
            "password": "@123456789Aa",
            "conform_password": "@123456789Aa"
        })

        self.assertEqual(response.status_code, 201)

        # checking in database
        self.assertTrue(
            User.objects.filter(email='user@example.com').exists()
        )





        