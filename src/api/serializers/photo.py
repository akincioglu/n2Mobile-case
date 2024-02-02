from rest_framework import serializers
from ..models.photo import Photo

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'albumId', 'title', 'url', 'thumbnailUrl']
