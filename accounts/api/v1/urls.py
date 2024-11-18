from django.urls import path

from .views import (
    Registrations,
    CustomAuthenticationsToken,
    CustomLogoutToken,
    CustomTokenObtainPairView,
    UserInformationShowing,
    UserChangePassWord,
    UserChangeEmail,
    UserChangeProfile,
    AuthenticatedUserInformation,
    ForgotPassword,
    ActivationAccount,
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # user registrations
    path("registration", Registrations.as_view(), name='Registrations_API'),
    path("authenticated-user-information", AuthenticatedUserInformation.as_view(), name='AuthenticatedUserInformation_API'),
    # user showing and edit account
    path("user/<int:pk>", UserInformationShowing.as_view(), name='UserInformationShowing_API'),
    path("user/<int:pk>/change-password", UserChangePassWord.as_view(), name='UserChangePassWord_API'),
    path("user/<int:pk>/change-email", UserChangeEmail.as_view(), name='UserChangeEmail_API'),
    path("user/<int:pk>/update-profile", UserChangeProfile.as_view(), name='UserChangeProfile_API'),
    # token authentications urls
    path("token/login/", CustomAuthenticationsToken.as_view(), name='CustomAuthenticationsToken_API'),
    path("token/logout/", CustomLogoutToken.as_view(), name='CustomLogoutToken_API'),
    # JWT authentications urls
    path("jwt/create/", CustomTokenObtainPairView.as_view(), name='CustomTokenObtainPairView_API'),
    path("jwt/refresh/", TokenRefreshView.as_view(), name='TokenRefreshView_API'),
    path("jwt/verify/", TokenVerifyView.as_view(), name='TokenVerifyView_API'),
    # forgot password and resent email for account activation
    path("resent-email/", ActivationAccount.as_view(), name='ActivationAccount_API'),
    path("forgot-password/", ForgotPassword.as_view(), name='ForgotPassword_API'),
]
