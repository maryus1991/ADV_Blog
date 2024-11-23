from django.urls import reverse, resolve
from django.test import TestCase, Client

from SiteSetting.views import ContactUS, AboutUS
from SiteSetting.models import Contact


class TestSiteSettingViewAndUrls(TestCase):

    def test_about_us_url_and_view(self):

        # get the client and url
        url = reverse("AboutUs")
        client = Client()

        # get the response and check the urls
        self.assertEqual(resolve(url).func.view_class, AboutUS)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_contact_us_url_and_view_with_valid_invalid_data(self):

        # get the client and url
        url = reverse("ContactUS")
        client = Client()

        # get the response in get method and check the url and view
        self.assertEqual(resolve(url).func.view_class, ContactUS)
        response = client.get(url).status_code
        self.assertEqual(response, 200)

        # test the url in post method and send data
        response = client.post(
            url,
            data={
                "full_name": "mez",
                "email": "test@test.com",
                "phone_number": "382398029831023",
                "subject": "test",
                "message": "test",
            },
        )
        self.assertEqual(response.status_code, 302)

        # check the data and check
        object_contact = Contact.objects.filter(phone_number="382398029831023").exists()
        self.assertTrue(object_contact)
