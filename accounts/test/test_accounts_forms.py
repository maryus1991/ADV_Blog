from django.test import TestCase
from datetime import datetime

from accounts.forms import (
    # *TestAuthorizationForms
    LoginForm,
    RegistrationForm,

    # *TestUpdateAccountForms
    ChangePasswordForm,
    UpdateProfileForm,
    SendMail_EmailField,
    UserSetPasswordForm,
    UpdateEmailForm,
)


class TestUpdateAccountForms(TestCase):
    """
    for testing the forms thats for updating and change the profile info
    """
    
    def test_update_profile_form_with_valid_and_invalid_data(self):
        
        # set the information for form
        form = UpdateProfileForm(
            {

                'first_name': 'mostafa',
                'last_name': 'ebrahim zadeh',                
            }
        )

        # validate the form
        self.assertTrue(form.is_valid())

        # check the form with invalid data
        self.assertFalse(UpdateProfileForm().is_valid()) 


    def test_send_mail_email_fields_form_with_valid_and_invalid_data(self):
        # send  data for form
        form = SendMail_EmailField(
            {
                'email': 'maryus19915123@gmail.com'
            }
        )

        # checking with assertions with valid and invalid status
        self.assertTrue(form.is_valid)
        self.assertFalse(SendMail_EmailField().is_valid())


    def test_change_password_form_with_valid_and_invalid_data(self):
        # ChangePasswordForm for change the user password in login status
        # send data to ChangePasswordForm
        form = ChangePasswordForm({
            'password': '@Aa123456789',
            'conform_password': '@Aa123456789',
        })

        # checking with assertions with valid and invalid status
        self.assertTrue(form.is_valid)
        self.assertFalse(ChangePasswordForm().is_valid())


    def test_the_current_password_form_with_valid_and_invalid_data(self):
        """
        UserSetPasswordForm     for changing user password with out sending email
        for form  thats needs to get and check the password 
        so i get the password for all choose forms in one fields 
        for not rewrite the password code 
        """ 
        
        # send data to UserSetPasswordForm
        form = UserSetPasswordForm({
            'current_password': '@Aa123456789',

        })

        # checking with assertions with valid and invalid status
        self.assertTrue(form.is_valid)
        self.assertFalse(UserSetPasswordForm().is_valid()) 


    def test_the_update_email_field_with_valid_and_invalid_data(self):
        
        # send data to UpdateEmailForm
        form = UpdateEmailForm({
            'email': 'maryus19915123@gmail.com'

        })

        # checking with assertions with valid and invalid status
        self.assertTrue(form.is_valid)
        self.assertFalse(UpdateEmailForm().is_valid()) 



class TestAuthorizationForms(TestCase):
    # for test the user authorization forms
    
    def test_login_form_with_valid_and_invalid_data(self):
        
        # send the data for login form
        form = LoginForm({
            'email': 'maryus19915123@gmail.com',
            'password': '@Aa12345678'
        })

        # check the form with valid and invalid data
        self.assertTrue(form.is_valid())
        self.assertFalse(LoginForm().is_valid())

    
    def test_registration_form_with_valid_and_invalid_data(self):
        # send the data for Registration form
        form = RegistrationForm({
            'email': 'maryus19915123@gmail.com',
            'password': '@Aa12345678',
            'conform_password': '@Aa12345678'
        })

        # check the form with valid and invalid data
        self.assertTrue(form.is_valid())
        self.assertFalse(RegistrationForm().is_valid())

        