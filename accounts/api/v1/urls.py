from django.urls import path

from .views import (Registrations, 
                    CustomAuthenticationsToken, 
                    CustomLogoutToken, 
                    CustomTokenObtainPairView)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('registrations', Registrations.as_view()),

    # token authentications urls
    path('token/login/', CustomAuthenticationsToken.as_view()),
    path('token/logout/', CustomLogoutToken.as_view()),

    # JWT authentications urls
    path('jwt/create/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', TokenRefreshView.as_view()),
    path('jwt/verify/', TokenVerifyView.as_view()),

]
