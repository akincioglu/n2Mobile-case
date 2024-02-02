from rest_framework import serializers
from ..models.album import Album

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'userId', 'title']
