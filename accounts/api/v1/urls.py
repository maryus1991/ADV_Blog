from django.urls import path

from .views import Registrations, CustomAuthenticationsToken, CustomLogoutToken

urlpatterns = [
    path('registrations', Registrations.as_view()),
    path('token/login/', CustomAuthenticationsToken.as_view()),
    path('token/logout/', CustomLogoutToken.as_view()),
]
