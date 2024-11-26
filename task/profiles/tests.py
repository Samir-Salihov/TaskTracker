from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User

class ProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword', fio='Test User')

    def test_get_profile(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
