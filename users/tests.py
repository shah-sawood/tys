from django.test import Client, TestCase

# Create your tests here.
class TestUserApp(TestCase):
    """tests the user app"""

    def check_status(self):
        client = Client()
        response = client.get("users/login/")

        self.assertEqual(response.status_code, 200)
