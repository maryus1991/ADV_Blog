from django.test import TestCase

from SiteSetting.models import SiteSetting, Contact

class TestContactUsModels(TestCase):

    def test_create_contact_us_model_with_invalid_data(self):
        
        # create object
        contact_us = Contact.objects.create(
            full_name = 'mez',        
            email = 'maryus19915123@gmail.com',        
            phone_number = '7898798987987',        
            subject = 'test',        
            message = 'test',            
        )

        # get again the object and check 
        contact_object = Contact.objects.get(id=contact_us.id)
        self.assertFalse(contact_object.is_read_by_admin)

