from django.test import TestCase

from accounts.models import User


class TestUserModel(TestCase):
    """
    Test User Model with unit test
    """

    def test_user_model_with_valid_data(self):

        # create user
        user = User.objects.create_user(email="admin@admin.com", password="@Aa123456")

        # get the user with create user object and check the information
        user_exist = User.objects.filter(
            id=user.id,
            email=user.email,
            is_active=True,
            is_staff=False,
            is_superuser=False,
            is_verified=False,
        ).exists()

        self.assertTrue(user_exist)
