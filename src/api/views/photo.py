from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from ..models.photo import Photo
from ..models.album import Album
from ..serializers.photo import PhotoSerializer

class PhotoViewSet(viewsets.ModelViewSet):
  serializer_class = PhotoSerializer

  def get_queryset(self):
    albumId = self.kwargs.get('albumId')
    queryset = Photo.objects.filter(albumId=albumId)
    return queryset
  
  def create(self, request, albumId=None):
    album = get_object_or_404(Album, id=albumId)
    data = request.data

    title = data.get('title', '')
    url = data.get('url', '')
    thumbnailUrl = data.get('thumbnailUrl', '')

    photo_data = {
      'albumId': album.id,
      'title': title,
      'url': url,
      'thumbnailUrl': thumbnailUrl
    }

    serializer = self.get_serializer(data=photo_data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)

    headers = self.get_success_headers(serializer.data)
    return Response(serializer.data, status=201, headers=headers)
  
  def update(self, request, albumId=None, photoId=None):
    album = get_object_or_404(Album, id=albumId)
    photo = get_object_or_404(Photo, id=photoId, albumId=album.id)

    data = request.data

    title = data.get('title', '')
    url = data.get('url', '')
    thumbnailUrl = data.get('thumbnailUrl', '')

    photo_data = {
      'title': title,
      'url': url,
      'thumbnailUrl': thumbnailUrl
    }

    serializer = self.get_serializer(photo, data=photo_data, partial=True)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)

    return Response(serializer.data)
  
  @action(detail=False, methods=['GET'])
  def get_photo_by_title(self, request, albumId=None):
      album = get_object_or_404(Album, id=albumId)
      title = self.request.query_params.get('title', '')
      photos = Photo.objects.filter(albumId=album.id, title__icontains=title)
      serializer = self.get_serializer(photos, many=True)
      return Response(serializer.data)