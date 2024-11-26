from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task, Comment
from users.models import User
from projects.models import Project


class TaskTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword', fio='Test User')
        self.project = Project.objects.create(name='Test Project', description='Test Description')
        self.task_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'project': self.project,  # Передаем объект Project
            'assignee': self.user,  # Передаем объект User
            'status': 'in_progress',
            'priority': 'high',
            'due_date': '2024-12-31T23:59:59Z'
        }
        self.task = Task.objects.create(**self.task_data)

    def test_create_task(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('task-list')
        response = self.client.post(url, {
            'title': 'New Task',
            'description': 'New Description',
            'project': self.project.id,  # Передаем идентификатор проекта
            'assignee': self.user.id,  # Передаем идентификатор пользователя
            'status': 'in_progress',
            'priority': 'high',
            'due_date': '2024-12-31T23:59:59Z'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_get_task(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('task-detail', args=[self.task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task_data['title'])

    def test_update_task(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('task-detail', args=[self.task.id])
        updated_data = {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'project': self.project.id,  # Передаем идентификатор проекта
            'assignee': self.user.id,  # Передаем идентификатор пользователя
            'status': 'done',
            'priority': 'medium',
            'due_date': '2024-12-31T23:59:59Z'
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, updated_data['title'])

    def test_delete_task(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('task-detail', args=[self.task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)


class CommentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword', fio='Test User')
        self.project = Project.objects.create(name='Test Project', description='Test Description')
        self.task = Task.objects.create(title='Test Task', description='Test Description', project=self.project,
                                        assignee=self.user)
        self.comment_data = {
            'task': self.task.id,
            'content': 'Test Comment'
        }
        self.comment = Comment.objects.create(task=self.task, author=self.user, content='Test Comment')

    def test_create_comment(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('comment-list')
        response = self.client.post(url, self.comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

    def test_get_comment(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('comment-detail', args=[self.comment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], self.comment_data['content'])

    def test_update_comment(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('comment-detail', args=[self.comment.id])
        updated_data = {
            'task': self.task.id,  # Добавляем идентификатор задачи
            'content': 'Updated Comment'
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, updated_data['content'])

    def test_delete_comment(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('comment-detail', args=[self.comment.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)
