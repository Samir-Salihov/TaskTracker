from rest_framework import serializers
from .models import Task, Comment
from users.models import User
from projects.models import Project


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'fio', 'role']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at', 'updated_at']


class TaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)
    tester = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'assignee', 'status', 'priority', 'created_at', 'updated_at',
                  'due_date', 'tester', 'comments']


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'assignee', 'status', 'priority', 'due_date', 'tester']


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'task', 'content']
        extra_kwargs = {
            'task': {'required': True},
            'content': {'required': True}
        }
