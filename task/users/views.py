from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import LogSerializer, RegSerializer, ProjectSerializer
from .models import User, Project


@api_view(['POST'])
def log_in_user(request):
    serializer = LogSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        if not user:
            return Response({"error": {"code": status.HTTP_401_UNAUTHORIZED,
                                       "message": "Authentication failed"}},
                            status=status.HTTP_401_UNAUTHORIZED)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'data': {"user_token": token.key}},
                        status=status.HTTP_200_OK)
    return Response({'error': {'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                               "message": "Validation error"}},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['POST'])
def sign_up_user(request):
    serializer = RegSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = Token.objects.create(user=user)
    return Response({'data': {"user_token": token.key}},
                    status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def log_out_user(request):
    if not request.user.is_active:
        return Response({"error": {"code": status.HTTP_403_FORBIDDEN,
                                   "message": "Login failed"}},
                        status=status.HTTP_403_FORBIDDEN)
    request.user.auth_token.delete()
    return Response({"data": {"message": "log out successfully"}},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_project(request):
    serializer = ProjectSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    project = serializer.save()
    request.user.current_projects.add(project)
    return Response({'data': {"project_id": project.id}},
                    status=status.HTTP_201_CREATED)
