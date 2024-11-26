from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task, Comment
from .serializers import TaskSerializer, TaskCreateUpdateSerializer, CommentSerializer, CommentCreateUpdateSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TaskCreateUpdateSerializer
        return TaskSerializer

    @action(detail=False, methods=['get'])
    def filter_tasks(self, request):
        queryset = self.get_queryset()
        title = request.query_params.get('title', None)
        status = request.query_params.get('status', None)
        priority = request.query_params.get('priority', None)
        assignee = request.query_params.get('assignee', None)
        created_at_from = request.query_params.get('created_at_from', None)
        created_at_to = request.query_params.get('created_at_to', None)
        updated_at_from = request.query_params.get('updated_at_from', None)
        updated_at_to = request.query_params.get('updated_at_to', None)
        due_date_from = request.query_params.get('due_date_from', None)
        due_date_to = request.query_params.get('due_date_to', None)

        if title:
            queryset = queryset.filter(title__icontains=title)
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        if assignee:
            queryset = queryset.filter(assignee__id=assignee)
        if created_at_from and created_at_to:
            queryset = queryset.filter(created_at__range=[created_at_from, created_at_to])
        if updated_at_from and updated_at_to:
            queryset = queryset.filter(updated_at__range=[updated_at_from, updated_at_to])
        if due_date_from and due_date_to:
            queryset = queryset.filter(due_date__range=[due_date_from, due_date_to])

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def sort_tasks(self, request):
        queryset = self.get_queryset()
        sort_by = request.query_params.get('sort_by', None)
        if sort_by == 'status':
            queryset = queryset.order_by('status')
        elif sort_by == 'priority':
            queryset = queryset.order_by('priority')
        elif sort_by == 'assignee':
            queryset = queryset.order_by('assignee__email')
        elif sort_by == 'created_at_asc':
            queryset = queryset.order_by('created_at')
        elif sort_by == 'created_at_desc':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'updated_at_asc':
            queryset = queryset.order_by('updated_at')
        elif sort_by == 'updated_at_desc':
            queryset = queryset.order_by('-updated_at')
        elif sort_by == 'due_date_asc':
            queryset = queryset.order_by('due_date')
        elif sort_by == 'due_date_desc':
            queryset = queryset.order_by('-due_date')

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CommentCreateUpdateSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
