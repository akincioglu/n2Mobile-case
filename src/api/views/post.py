from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from ..models.post import Post
from ..models.user import User
from ..serializers.post import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
  serializer_class = PostSerializer

  def get_queryset(self):
      userId = self.kwargs.get('userId')
      queryset = Post.objects.filter(userId=userId)
      return queryset

  def create(self, request, userId=None):
      user = get_object_or_404(User, id=userId)
      data = request.data

      title = data.get('title', '')
      body = data.get('body', '')

      post_data = {
          'user': user.id,
          'title': title,
          'body': body
      }

      serializer = self.get_serializer(data=post_data)
      serializer.is_valid(raise_exception=True)
      self.perform_create(serializer)

      headers = self.get_success_headers(serializer.data)
      return Response(serializer.data, status=201, headers=headers)
  
  def update(self, request, userId=None, pk=None):
      user = get_object_or_404(User, id=userId)
      post = get_object_or_404(Post, id=pk, userId=user.id)

      data = request.data
      title = data.get('title', post.title)
      body = data.get('body', post.body)

      post_data = {
          'user': user.id,
          'title': title,
          'body': body
      }

      serializer = self.get_serializer(post, data=post_data, partial=True)
      serializer.is_valid(raise_exception=True)
      self.perform_update(serializer)

      return Response(serializer.data)
  
  @action(detail=False, methods=['GET'])
  def get_post_by_title(self, request, userId=None):
      user = get_object_or_404(User, id=userId)
      title = self.request.query_params.get('title', '')
      posts = Post.objects.filter(userId=user.id, title__icontains=title)
      serializer = self.get_serializer(posts, many=True)
      return Response(serializer.data)