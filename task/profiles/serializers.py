from rest_framework import serializers
from .models import User, Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description']

class UserProfileSerializer(serializers.ModelSerializer):
    current_projects = ProjectSerializer(many=True, read_only=True)
    project_history = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'avatar', 'role', 'current_projects', 'project_history']
