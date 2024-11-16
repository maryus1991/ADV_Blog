from django.test import TestCase

from SiteSetting.forms import ContactModelForm

class TestContactFrom(TestCase):
    def test_contact_us_with_valid_and_invalid_data(self):
        
        # send the data to from 
        form = ContactModelForm({

            'full_name':'mez',
            'email':'test@test.com',
            'phone_number':'789456123',
            'subject':'test',
            'message':'test',            
        })


        # check 
        self.assertTrue(form.is_valid())
        self.assertFalse(ContactModelForm().is_valid())
        