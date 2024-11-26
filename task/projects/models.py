# # projects/models.py
#
# from django.db import models
# from django.utils import timezone
# from users.models import User
#
# class Project(models.Model):
#     STATUS_CHOICES = [
#         ('active', 'Активен'),
#         ('archived', 'Архивирован'),
#     ]
#
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
#     members = models.ManyToManyField(User, related_name='projects')
#
#     def __str__(self):
#         return self.name


from django.db import models
from users.models import User

class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активен'),
        ('archived', 'Архивирован'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    members = models.ManyToManyField(User, related_name='projects')  # Новое поле без промежуточной модели

    def __str__(self):
        return self.name