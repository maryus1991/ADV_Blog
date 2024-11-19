from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

import pytest


from accounts.models import User


user_options = {
    "email": "admin@admin.domain",
    "password": "@Aa1234567890",
}



@pytest.fixture
def client():

    # create user  
    user = User.objects.create_user(
        email = user_options.get('email'),
        password = user_options.get('password')     
    ) 

    user.is_verified = True
    user.is_active = True
    user.verified_code = get_random_string(255)
    user.save()

    # create anonymous and logged in request

    anonymous_client = APIClient()

    client = APIClient()


    # get jwt token and check
    jwt_url = reverse('CustomTokenObtainPairView_API')

    result = client.post(jwt_url, user_options)
    assert result.status_code == 200

    jwt_token = result.json().get('access') 

    # set the header
    headers = {"HTTP_AUTHORIZATION": "Bearer " + jwt_token}
    client.credentials(**headers)

    """
    the return is about three section in tuple the first is the jwt token in header client the second is the response for getting
    jwt tokens and the third is for sending anonymous requests and for forth option is user 
    """
    return (client, anonymous_client, result.json(), user)

        
@pytest.mark.django_db
class TestAccountAuthenticatedApi:

    def test_registration_api_url_with_valid_data(self, client):

        # get the url
        url = reverse('Registrations_API')

        # send request with valid data
        response = client[1].post(url, {
            "email": "user@example.com",
            "first_name": "mostafa",
            "last_name": "khenifary",
            "password": "@123456789Aa",
            "conform_password": "@123456789Aa"
        })

        assert response.status_code == 201

        # checking in database
        assert User.objects.filter(email='user@example.com').exists() == True
        
    def test_jwt_verify_url_and_jwt_refresh_url_with_valid_and_invalid_user_information(self, client):

        # get the urls
        refresh_url= reverse('TokenRefreshView_API')
        verify_url= reverse('TokenVerifyView_API')

        # send requests with valid data
        refresh_url_response = client[1].post(refresh_url, {'refresh': client[2].get('refresh')})
        verify_url_response = client[1].post(verify_url, {'token': client[2].get('access')})

        # check the requests
        assert verify_url_response.status_code == 200
        assert refresh_url_response.status_code == 200        

        # test with invalid data

        verify_url_response = client[1].post(verify_url, {'token': get_random_string(255)})
        refresh_url_response = client[1].post(refresh_url, {'refresh': get_random_string(255)})
    
        assert verify_url_response.status_code == 401
        assert refresh_url_response.status_code == 401  

    def test_login_and_logout_token_authentication_and_get_user_information_urls_with_user_information(self, client):

        # get the urls
        CustomAuthenticationsToken_API_url = reverse('CustomAuthenticationsToken_API')        
        CustomLogoutToken_API_url = reverse('CustomLogoutToken_API')
        AuthenticatedUserInformation_API_url = reverse('AuthenticatedUserInformation_API')

        # get the token from token login api
        CustomAuthenticationsToken_API_response = client[1].post(CustomAuthenticationsToken_API_url, user_options)

        # check the status code and get the token
        assert CustomAuthenticationsToken_API_response.status_code == 200

        token = CustomAuthenticationsToken_API_response.json().get('token')

        # check the token in db
        token = Token.objects.get(key=token)

        assert (token is not None) == True

        # send request for logout
        # set headers 
        login_client = client[1]
        
        login_client.credentials(**{"HTTP_AUTHORIZATION": "Token " + token.key})

        # check user authenticated with AuthenticatedUserInformation url
        response = login_client.get(AuthenticatedUserInformation_API_url)
        assert response.status_code == 202

        # logout the request
        response = login_client.post(CustomLogoutToken_API_url)

        assert response.status_code == 204

        # check the token in db 
        token = Token.objects.filter(key=token.key).exists()

        assert token == False
        
    def test_user_change_password_and_user_change_email_and_user_update_profile_and_get_user_information_urls_with_valid_data(self, client):

        # get the urls

        UserInformationShowing_API_url = reverse('UserInformationShowing_API', kwargs={'pk': client[3].pk})        
        UserChangePassWord_API_url = reverse('UserChangePassWord_API', kwargs={'pk': client[3].pk})
        UserChangeEmail_API_url = reverse('UserChangeEmail_API', kwargs={'pk': client[3].pk})
        UserChangeProfile_API_url = reverse('UserChangeProfile_API', kwargs={'pk': client[3].pk})

        # *check the client if it login and test get user information
        response = client[0].get(UserInformationShowing_API_url)

        # check the status code and email in db
        assert response.status_code == 200
        assert User.objects.filter(email=response.json().get('email')).exists() == True

        # test user change password 
        response = client[0].put(UserChangePassWord_API_url, {
            "password": '@Aa1234567890' ,
            "new_password": "@!£Aa189",
            "conform_new_password": "@!£Aa189"
        })

        # check the status code
        assert response.status_code == 202
        
        # check the db
        assert User.objects.get(id=client[-1].id).check_password('@!£Aa189') == True

        # *change user email
        # send request
        response = client[0].put(UserChangeEmail_API_url, {'email': 'admin@amdin.admin'})

        # check the request and check in db
        assert response.status_code == 200

        assert User.objects.filter(email=user_options.get('email')).exists() == False
        assert client[0].put(UserChangeEmail_API_url, {'email': user_options.get('email')}).status_code == 200

        # check user verify and verify the user
        user = User.objects.filter(email=user_options.get('email')).first()
        assert user.is_verified == False
        user.is_verified = True
        user.save()


        # * User update Profile
        # send request and check the db
        response = client[0].put(UserChangeProfile_API_url,
                {
                    "first_name": "mez",
                    "last_name": "mez"
                }
        )

        assert response.status_code == 202

        # get the user info form url and check it with db for test
        get_user_info_response = client[0].get(UserInformationShowing_API_url)

        assert get_user_info_response.status_code == 200
        user = User.objects.get(id=client[-1].id)

        assert user.first_name == get_user_info_response.json().get('first_name')
        assert user.last_name == get_user_info_response.json().get('last_name')

    def test_forgot_password_and_rent_email_api_with_anonymous_request_and_valid_data(self, client):

        # get the url
        resent_email_api_url = reverse('ActivationAccount_API')
        ForgotPassword_API_url = reverse('ForgotPassword_API')        
        
        # *test the forgot passwrod api
        # send request
        response = client[1].post(
            ForgotPassword_API_url, 
            {
                'email': user_options.get('email')
            }
        )

        # check the status code
        assert response.status_code == 202

        # *test resent email
        # send request
        response = client[1].post(
                resent_email_api_url,
                {
                    'email': user_options.get('email')
                }
        )
        
        # check the status code
        assert response.status_code == 202
