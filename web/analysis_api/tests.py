from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.authtoken import views
from django.contrib.auth.models import User






class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="Chris", password="1234")


    def test_auth_analysis(self):
    # Include an appropriate `Authorization:` header on all requests.

        token = views.obtain_auth_token(username="Chris", password="1234")
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get('http://localhost:8000/api/v1/analysis')
        self.assertEqual(response.status_code, 200)


