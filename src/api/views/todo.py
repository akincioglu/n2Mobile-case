from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from ..models.todo import Todo
from ..models.user import User
from ..serializers.todo import TodoSerializer

class TodoViewSet(viewsets.ModelViewSet):
  serializer_class = TodoSerializer

  def get_queryset(self):
      userId = self.kwargs.get('userId')
      queryset = Todo.objects.filter(userId=userId)
      return queryset
  
  def create(self, request, userId=None):
      user = get_object_or_404(User, id=userId)
      data = request.data

      title = data.get('title', '')

      todo_data = {
          'userId': user.id,
          'title': title,
      }

      serializer = self.get_serializer(data=todo_data)
      serializer.is_valid(raise_exception=True)
      self.perform_create(serializer)

      headers = self.get_success_headers(serializer.data)
      return Response(serializer.data, status=201, headers=headers)
  
  def update(self, request, userId=None, pk=None):
      user = get_object_or_404(User, id=userId)
      todo = get_object_or_404(Todo, id=pk, userId=user.id)

      data = request.data
      title = data.get('title', todo.title)

      todo_data = {
          'user': user.id,
          'title': title
      }

      serializer = self.get_serializer(todo, data=todo_data, partial=True)
      serializer.is_valid(raise_exception=True)
      self.perform_update(serializer)

      return Response(serializer.data)
  
  @action(detail=False, methods=['GET'])
  def get_todo_by_title(self, request, userId=None):
      user = get_object_or_404(User, id=userId)
      title = self.request.query_params.get('title', '')
      todos = Todo.objects.filter(userId=user.id, title__icontains=title)
      serializer = self.get_serializer(todos, many=True)
      return Response(serializer.data)
  
  @action(detail=True, methods=['POST'])
  def mark_as_completed(self, request, userId=None, pk=None):
      user = get_object_or_404(User, id=userId)
      todo = get_object_or_404(Todo, id=pk, userId=user.id)

      todo.completed = True
      todo.save()

      serializer = self.get_serializer(todo)
      return Response(serializer.data)