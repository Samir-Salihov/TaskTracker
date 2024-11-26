from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Project
from users.models import User

class ProjectTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword', fio='Test User')
        self.project_data = {
            'name': 'Test Project',
            'description': 'Test Description'
        }
        self.project = Project.objects.create(**self.project_data)

    def test_create_project(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('project-list')
        response = self.client.post(url, self.project_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)

    def test_get_project(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('project-detail', args=[self.project.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.project_data['name'])

    def test_update_project(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('project-detail', args=[self.project.id])
        updated_data = {'name': 'Updated Project'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, updated_data['name'])

    def test_delete_project(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('project-detail', args=[self.project.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)
