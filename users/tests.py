"""user app test layer"""
from django.test import Client, TestCase

# Create your tests here.
class TestUserApp(TestCase):
    """tests the user app"""

    def check_status(self):
        """check the status of login page"""
        client = Client()
        response = client.get("users/login/")

        self.assertEqual(response.status_code, 200)
