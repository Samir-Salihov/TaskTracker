from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .models import User


class UserTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'fio': 'Test User',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'developer'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.token = Token.objects.create(user=self.user)

    # def test_signup_user(self):
    #     url = reverse('signup')
    #     response = self.client.post(url, self.user_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(User.objects.count(), 2)
    # def test_signup_user(self):
    #     url = reverse('signup')
    #     user_data = {
    #         'email': 'newuser@example.com',
    #         'password': 'newpassword',
    #         'fio': 'New User',
    #         'first_name': 'New',
    #         'last_name': 'User',
    #         'role': 'developer'
    #     }
    #     response = self.client.post(url, user_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(User.objects.count(), 2)

    def test_login_user(self):
        url = reverse('login')
        response = self.client.post(url, {'email': 'test@example.com', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user_token', response.data['data'])

    def test_logout_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['message'], 'log out successfully')
