from django.urls import path

from .views import (Registrations, 
                    CustomAuthenticationsToken, 
                    CustomLogoutToken, 
                    CustomTokenObtainPairView,
                    UserInformationShowing,
                    UserChangePassWord,
                    UserChangeEmail,
                    )

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [

    # user registrations
    path('registrations', Registrations.as_view()),

    # user showing and edit account
    path('user/<int:pk>', UserInformationShowing.as_view()),
    path('user/<int:pk>/change-password', UserChangePassWord.as_view()),
    path('user/<int:pk>/change-email', UserChangeEmail.as_view()),

    # token authentications urls
    path('token/login/', CustomAuthenticationsToken.as_view()),
    path('token/logout/', CustomLogoutToken.as_view()),

    # JWT authentications urls
    path('jwt/create/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', TokenRefreshView.as_view()),
    path('jwt/verify/', TokenVerifyView.as_view()),

]
