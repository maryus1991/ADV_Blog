from django.urls import reverse
from rest_framework.test import APIClient
import pytest

from SiteSetting.models import Contact


@pytest.mark.django_db
class TestSiteSetting:

    def test_create_contact_by_user_and_get_site_setting_api(self):

        # get the urls and client
        CreateContactView_url = reverse("CreateContactView")
        SiteSettingView_url = reverse("SiteSettingView")
        client = APIClient()

        data = {
            "full_name": "mez",
            "email": "user@example.com",
            "phone_number": "1234567890",
            "subject": "test",
            "message": "test",
        }

        # test create contact
        response = client.post(CreateContactView_url, data)

        # check the status code and in db
        assert response.status_code == 201
        assert (
            Contact.objects.filter(
                full_name=data.get("full_name"),
                email=data.get("email"),
                phone_number=data.get("phone_number"),
                subject=data.get("subject"),
            ).exists()
            == True
        )

        # get site setting
        response = client.get(SiteSettingView_url)
        assert response.status_code == 200
