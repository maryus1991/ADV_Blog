from django.urls import reverse, resolve
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from accounts.views import (Authorizations, Dashboard, Registrations,
ConformAccount, ForgotPassword_Token,ForgotPassword, ChangePassword, 
                                UpdateProfile,ChangeEmail ,ResentEmail)

User = get_user_model()


class TestAccountsUrls(TestCase):
    # for test the accounts blog urls

    def setUp(self):
        """
        create a user in test db for test the urls 
        """
        user = User.objects.create_user(
            email= 'admin@admin.domain',
            password= '@Aa1234567890' 
        )

        user.verified_code = get_random_string(255)
        user.save()


    def test_dashboard_url_with_login_and_anonymous_requests(self):
        
        # check the url with View
        url = reverse('Dashboard')
        self.assertEqual(resolve(url).func.view_class, Dashboard)

        # get the url and check the anonymous 
        # request should be redirect to Authorize page
        # check the status code

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        
        # check the request with login request and check the status code
        client =  Client()
        client.login(email='admin@admin.domain',  
                    password='@Aa1234567890')   

        response = client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_authorize_page_with_login_and_anonymous_requests(self):
        
        # get and check the urls with views
        url = reverse('Authorizations')
        self.assertEqual(resolve(url).func.view_class, Authorizations)

        client = Client()

        # check the url with anonymous request
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        # check the url with request login request
        client =  Client()
        client.login(email='admin@admin.domain',  
                    password='@Aa1234567890')   

        response = client.get(url)
        self.assertEqual(response.status_code, 302)


    def test_registrations_urls_with_post_method_and_valid_and_invalid_data(self):
        
        # get and check the url with view
        url = reverse('Registrations')
        self.assertEqual(resolve(url).func.view_class, Registrations)

        client = Client()
        
        # send requsst with post method 
        response = client.post(
            url,
            data={
                'email': 'maryus19915123@gmail.com',
                'password': '@Aa1234567890', 
                'conform_password': '@Aa1234567890', 
            }
        )
        self.assertEqual(response.status_code, 302) # check the post request with sended data 
        self.assertEqual(client.get(url).status_code, 302) # check the get method with request 
        self.assertEqual(client.post(url).status_code, 302) # check the post method with invalid data 


    def test_login_urls_with_post_and_get_method_with_valid_and_invalid_data(self):
        url = reverse('Login')
        client = Client()

        # set the data 
        response = client.post(
            url, 
            data = {
                'email': 'admin@admin.domain',
                'password': '@Aa1234567890'
            }
        )

        self.assertEqual(response.status_code, 302) # check the post request with sended data 
        self.assertEqual(client.get(url).status_code, 302) # check the get method with request 
        self.assertEqual(client.post(url).status_code, 302) # check the post method with invalid data 


    def test_logout_urls_with_post_and_get_method(self):
        url = reverse('Logout')    

        # get a client for logout for both urls get and post
        client = Client()
        
        # anonymous request
        self.assertEqual(client.post(url).status_code, 302)


        # logged in client
        client.login(email='admin@admin.domain',  
                    password='@Aa1234567890')   

        # check the urls with get and post method 
        self.assertEqual(client.get(url).status_code, 302)
        self.assertEqual(client.post(url).status_code, 302)
    
    
    def test_conform_account_urls_and_check_with_user_verify_account(self):
        # get the user and verify code and get the url

        user = User.objects.get(email='admin@admin.domain')

        # get and check the url with view
        url = reverse('ConformAccount', kwargs={'token': user.verified_code})
        self.assertEqual(resolve(url).func.view_class, ConformAccount)

        # check the status code
        self.assertEqual(self.client.get(url).status_code, 302)
        
        user = User.objects.get(email='admin@admin.domain')

        # check the user account should be verify
        self.assertTrue(user.is_verified)
    

    def test_forgot_password_urls_and_check_the_user_password(self):
        
        # get the urls
        forqot_password_url = reverse('ForgotPassword')
        
        # get the clients
        anonymous_client = Client()
        login_client = Client()

        login_client.login(email='admin@admin.domain',  
                    password='@Aa1234567890')
        
        # check it with login in user and anonymous requests
        self.assertEqual(login_client.get(forqot_password_url).status_code, 302)
        self.assertEqual(anonymous_client.get(forqot_password_url).status_code, 200)

        # check the post method in forgot pass url
        response = anonymous_client.post(forqot_password_url, data={
            'email': 'maryus19915123@gmail.com'
        })
        self.assertEqual(response.status_code, 302)

        # get the user and password and forgot password token url
        user = User.objects.get(email='admin@admin.domain')

        
        # check the url with view
        token_url = reverse('ForgotPassword_token', kwargs={'token': user.verified_code})
        self.assertEqual(resolve(token_url).func.view_class, ForgotPassword_Token)
        self.assertEqual(resolve(forqot_password_url).func.view_class, ForgotPassword)

        
        # check the token url with logged in request and wrong token
        self.assertEqual(login_client.get(token_url).status_code, 302)
        self.assertEqual(anonymous_client.post(reverse('ForgotPassword_token', kwargs={'token':get_random_string(255)})).status_code, 302)
        
        # check the post method and passwords
        response = anonymous_client.post(token_url, data={
            'password': "@Ee!$%^&*()1234",
            'conform_password': "@Ee!$%^&*()1234",
        })
        self.assertEqual(response.status_code, 302)

        # get the user again
        user = User.objects.get(email='admin@admin.domain')

        # check the user password is changed or not
        self.assertTrue(user.check_password('@Ee!$%^&*()1234'))
    

    def test_update_password_and_update_profile_urls_with_user_data(self):
        
        # get the urls and check
        change_password_url = reverse('ChangePassword')
        update_profile_url  = reverse('UpdateProfile')

        self.assertEqual(resolve(change_password_url).func.view_class, ChangePassword)
        self.assertEqual(resolve(update_profile_url).func.view_class, UpdateProfile)


        # get the clients and user
        anonymous_client = Client()
        login_client = Client()

        login_client.login(email='admin@admin.domain',  
                    password='@Aa1234567890')
        
        user = User.objects.get(email='admin@admin.domain')

        # check the urls with anonymous request
        self.assertEqual(anonymous_client.post(change_password_url).status_code, 302)
        self.assertEqual(anonymous_client.post(update_profile_url).status_code, 302)

        # check it with logged in url and send information 

        update_profile_url_response = login_client.post(update_profile_url,
        data={
                'first_name': 'kazem',        
                'last_name': 'yesman',
                'avatar': ''                
        })


        change_password_url_response = login_client.post(change_password_url,
            data={
                'current_password': '@Aa1234567890',
                'password': '@!"£$%^&*()_+123aA',
                'conform_password': '@!"£$%^&*()_+123aA' ,
            }
        ) 



        self.assertEqual(change_password_url_response.status_code, 302)
        self.assertEqual(update_profile_url_response.status_code, 302)

        # check if the user information change or not
        user_updated_information = User.objects.get(email='admin@admin.domain')
        
        self.assertTrue(user_updated_information.check_password('@!"£$%^&*()_+123aA'))
        self.assertNotEqual(user.first_name, user_updated_information.first_name)
        self.assertNotEqual(user.last_name, user_updated_information.last_name)


    def test_change_email_and_resent_email_urls_with_user_data(self):
        
        # get and check the urls

        ChangeEmail_url = reverse('ChangeEmail')
        ResentEmail_url = reverse('ResentEmail')
        self.assertEqual(resolve(ChangeEmail_url).func.view_class, ChangeEmail)
        self.assertEqual(resolve(ResentEmail_url).func.view_class, ResentEmail)



        # get the clients and user
        anonymous_client = Client()
        login_client = Client()

        login_client.login(email='admin@admin.domain',  
                    password='@Aa1234567890')
        
        user = User.objects.get(email='admin@admin.domain')
        verify_code = user.verified_code

        # check the urls with anonymous request
        self.assertEqual(anonymous_client.post(ChangeEmail_url).status_code, 302)
        self.assertEqual(anonymous_client.post(ResentEmail_url).status_code, 302)

        # check the change email
        response = login_client.post(ChangeEmail_url, data={
            'email': 'admin@admin.domain'
        })

        self.assertEqual(response.status_code, 302)

        # check the user information 
        user = User.objects.get(email='admin@admin.domain')#
        self.assertFalse(user.is_verified)
        self.assertNotEqual(user.is_verified, verify_code)

