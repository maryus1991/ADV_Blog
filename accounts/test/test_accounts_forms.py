from django.test import TestCase
from datetime import datetime

from accounts.forms import (
    ChangePasswordForm,
    LoginForm,
    RegistrationForm,
    SendMail_EmailField,
    UpdateEmailForm,
    UpdateProfileForm,
    UserSetPasswordForm,
)


class TestUpdateAccountForms(TestCase):
    """
    for testing the forms thats for updating and change the profile info
    """
    
    def test_update_profile_form_with_valid_and_invalid_data(self):
        pass


class TestAuthorizationForms(TestCase):
    pass