from django.urls import path, include


from .views import (
    Dashboard,
    Authorizations,
    Registrations,
    Login,
    Logout,
    ConformAccount,
    ForgotPassword,
    ForgotPassword_Token,
    ChangePassword,
    ChangeEmail,
    UpdateProfile,
    ResentEmail,
)

urlpatterns = [
    path("", Dashboard.as_view(), name="Dashboard"),
    path(
        "authorize/",
        Authorizations.as_view(),
        name="Authorizations",
    ),
    path("register/", Registrations.as_view(), name="Registrations"),
    path("login/", Login.as_view(), name="Login"),
    path("logout/", Logout.as_view(), name="Logout"),
    path("conform/<token>", ConformAccount.as_view(), name="ConformAccount"),
    path(
        "forgot-password/",
        ForgotPassword.as_view(),
        name="ForgotPassword",
    ),
    path(
        "forgot-password/<token>",
        ForgotPassword_Token.as_view(),
        name="ForgotPassword_token",
    ),
    path("change-password", ChangePassword.as_view(), name="ChangePassword"),
    path("update-profile", UpdateProfile.as_view(), name="UpdateProfile"),
    path("change-email", ChangeEmail.as_view(), name="ChangeEmail"),
    path(
        "resent-email",
        ResentEmail.as_view(),
        name="ResentEmail",
    ),
    path("api/v1/", include("accounts.api.v1.urls")),
]
