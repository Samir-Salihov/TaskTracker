# # projects/views.py
#
# from rest_framework import viewsets, permissions, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from .models import Project
# from .serializers import ProjectSerializer, ProjectCreateUpdateSerializer
# from users.models import User
#
#
# class ProjectViewSet(viewsets.ModelViewSet):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
#
#     # permission_classes = [permissions.IsAuthenticated]
#
#     def get_serializer_class(self):
#         if self.action in ['create', 'update', 'partial_update']:
#             return ProjectCreateUpdateSerializer
#         return ProjectSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         project = serializer.save()
#         headers = self.get_success_headers(serializer.data)
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         project = serializer.save()
#
#         return Response(serializer.data)
#
#     @action(detail=True, methods=['post'])
#     def add_member(self, request, pk=None):
#         project = self.get_object()
#         user_id = request.data.get('user_id')
#         try:
#             user = User.objects.get(id=user_id)
#             project.members.add(user)
#             return Response({'status': 'member added'})
#         except User.DoesNotExist:
#             return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
#
#     @action(detail=True, methods=['post'])
#     def remove_member(self, request, pk=None):
#         project = self.get_object()
#         user_id = request.data.get('user_id')
#         try:
#             user = User.objects.get(id=user_id)
#             project.members.remove(user)
#             return Response({'status': 'member removed'})
#         except User.DoesNotExist:
#             return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
#
#     @action(detail=False, methods=['get'])
#     def filter_projects(self, request):
#         queryset = self.get_queryset()
#         name = request.query_params.get('name', None)
#         status = request.query_params.get('status', None)
#         created_at_from = request.query_params.get('created_at_from', None)
#         created_at_to = request.query_params.get('created_at_to', None)
#         updated_at_from = request.query_params.get('updated_at_from', None)
#         updated_at_to = request.query_params.get('updated_at_to', None)
#
#         if name:
#             queryset = queryset.filter(name__icontains=name)
#         if status:
#             queryset = queryset.filter(status=status)
#         if created_at_from and created_at_to:
#             queryset = queryset.filter(created_at__range=[created_at_from, created_at_to])
#         if updated_at_from and updated_at_to:
#             queryset = queryset.filter(updated_at__range=[updated_at_from, updated_at_to])
#
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
#
#     @action(detail=False, methods=['get'])
#     def sort_projects(self, request):
#         queryset = self.get_queryset()
#         sort_by = request.query_params.get('sort_by', None)
#         if sort_by == 'created_at_asc':
#             queryset = queryset.order_by('created_at')
#         elif sort_by == 'created_at_desc':
#             queryset = queryset.order_by('-created_at')
#         elif sort_by == 'updated_at_asc':
#             queryset = queryset.order_by('updated_at')
#         elif sort_by == 'updated_at_desc':
#             queryset = queryset.order_by('-updated_at')
#         elif sort_by == 'name_asc':
#             queryset = queryset.order_by('name')
#         elif sort_by == 'name_desc':
#             queryset = queryset.order_by('-name')
#
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)



# projects/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer, ProjectCreateUpdateSerializer
from users.models import User

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProjectCreateUpdateSerializer
        return ProjectSerializer

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            project.members.add(user)
            return Response({'status': 'member added'})
        except User.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            project.members.remove(user)
            return Response({'status': 'member removed'})
        except User.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def filter_projects(self, request):
        queryset = self.get_queryset()
        name = request.query_params.get('name', None)
        status = request.query_params.get('status', None)
        created_at_from = request.query_params.get('created_at_from', None)
        created_at_to = request.query_params.get('created_at_to', None)
        updated_at_from = request.query_params.get('updated_at_from', None)
        updated_at_to = request.query_params.get('updated_at_to', None)

        if name:
            queryset = queryset.filter(name__icontains=name)
        if status:
            queryset = queryset.filter(status=status)
        if created_at_from and created_at_to:
            queryset = queryset.filter(created_at__range=[created_at_from, created_at_to])
        if updated_at_from and updated_at_to:
            queryset = queryset.filter(updated_at__range=[updated_at_from, updated_at_to])

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def sort_projects(self, request):
        queryset = self.get_queryset()
        sort_by = request.query_params.get('sort_by', None)
        if sort_by == 'created_at_asc':
            queryset = queryset.order_by('created_at')
        elif sort_by == 'created_at_desc':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'updated_at_asc':
            queryset = queryset.order_by('updated_at')
        elif sort_by == 'updated_at_desc':
            queryset = queryset.order_by('-updated_at')
        elif sort_by == 'name_asc':
            queryset = queryset.order_by('name')
        elif sort_by == 'name_desc':
            queryset = queryset.order_by('-name')

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)