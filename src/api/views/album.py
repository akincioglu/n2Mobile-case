from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from ..models.album import Album
from ..models.user import User
from ..serializers.album import AlbumSerializer

class AlbumViewSet(viewsets.ModelViewSet):
  serializer_class = AlbumSerializer

  def get_queryset(self):
      userId = self.kwargs.get('userId')
      queryset = Album.objects.filter(userId=userId)
      return queryset
  
  def create(self, request, userId=None):
      user = get_object_or_404(User, id=userId)
      data = request.data

      title = data.get('title', '')

      album_data = {
          'user': user.id,
          'title': title
      }

      serializer = self.get_serializer(data=album_data)
      serializer.is_valid(raise_exception=True)
      self.perform_create(serializer)

      headers = self.get_success_headers(serializer.data)
      return Response(serializer.data, status=201, headers=headers)
  
  def update(self, request, userId=None, albumId=None):
      user = get_object_or_404(User, id=userId)
      album = get_object_or_404(Album, id=albumId, userId=user.id)

      data = request.data
      title = data.get('title', album.title)

      album_data = {
          'user': user.id,
          'title': title
      }

      serializer = self.get_serializer(album, data=album_data, partial=True)
      serializer.is_valid(raise_exception=True)
      self.perform_update(serializer)

      return Response(serializer.data)
  
  @action(detail=False, methods=['GET'])
  def get_album_by_title(self, request, userId=None):
      user = get_object_or_404(User, id=userId)
      title = self.request.query_params.get('title', '')
      albums = Album.objects.filter(userId=user.id, title__icontains=title)
      serializer = self.get_serializer(albums, many=True)
      return Response(serializer.data)