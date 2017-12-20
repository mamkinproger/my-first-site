from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status


class AccountsTest(APITestCase):

    def SetUp(self):
        self.test_user = User.objects.create_user('testuser', 'testuser@mail.ru', 'testpassword')
        self.test_create_user()

    def test_create_user(self):
        url = reverse('signup')
        data = {
            'username': 'test7',
            'email': 'test7@mail.ru',
            'password': '123456'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)
