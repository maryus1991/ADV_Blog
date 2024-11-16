from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import pytest

User = get_user_model()

user = {
    "email": "admin@admin.domain",
    "password": "@Aa1234567890",
}

@pytest.fixture
def client():
    """
    create and get APIClient with jwt token in headers for auth user that tested for jwt token apis
    """
    client = APIClient()
    User.objects.create_user(
        email=user.get("email"), password=user.get("password")
    )
    response = client.post(
        reverse('CustomTokenObtainPairView'),
        {
            "email": user.get("email"),
            "password": user.get("password"),
        },
    )

    print(response.json().get("access"))
    headers = {"HTTP_AUTHORIZATION": "Bearer " + response.json().get("access")}
    assert response.status_code == 201
    client.credentials(**headers)
    """
    the return is about three section in tuple the first is the jwt 
    token in header client the second is the response for getting
    jwt tokens and the third is for senf=ding anonymous requests
    """
    return (client, response.json(), APIClient())


@pytest.mark.django_db
class TestUserAuthenticationsAPI:
    '''
    for test user login, registration, reset email, forgot password, api 
    '''
    pass
