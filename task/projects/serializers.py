from rest_framework import serializers
from .models import Project
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'fio', 'role']

class ProjectSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'status', 'members']

class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'status']
