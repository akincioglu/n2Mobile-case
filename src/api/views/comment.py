from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from ..models.comment import Comment
from ..models.user import User
from ..models.post import Post
from ..serializers.comment import CommentSerializer

class CommentViewSet(viewsets.ModelViewSet):
  serializer_class = CommentSerializer

  def get_queryset(self):
    userId = self.kwargs.get('userId')
    postId = self.kwargs.get('postId')
    queryset = Comment.objects.filter(postId=postId)
    return queryset
  
  def create(self, request, userId=None, postId=None):
    post = get_object_or_404(Post, id=postId)

    data = request.data

    name = data.get('name', '')
    email = data.get('email', '')
    body = data.get('body', '')

    comment_data = {
      'postId': post.id,
      'name': name,
      'email': email,
      'body': body
    }

    serializer = self.get_serializer(data=comment_data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)

    headers = self.get_success_headers(serializer.data)
    return Response(serializer.data, status=201, headers=headers)
  
  def update(self, request, postId=None, pk=None):
    post = get_object_or_404(Post, id=postId)
    comment = get_object_or_404(Comment, id=pk, postId=post.id)

    data = request.data

    body = data.get('body', '')

    comment_data = {
      'postId': post.id,
      'body': body
    }
    
    serializer = self.get_serializer(comment, data=comment_data, partial=True)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)

    return Response(serializer.data)