from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User, Project


class LogSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
        attrs['user'] = user
        return attrs


class RegSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=12, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'fio', 'first_name', 'last_name', 'role']
        extra_kwargs = {
            'email': {'required': True},
            'password': {'required': True},
            'fio': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'role': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            fio=validated_data['fio'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', '')
        )
        return user


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description']
