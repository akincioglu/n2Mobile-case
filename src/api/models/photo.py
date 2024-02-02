from django.db import models
from .album import Album

class Photo(models.Model):
    albumId = models.ForeignKey(Album, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url = models.URLField()
    thumbnailUrl = models.URLField()

    def __str__(self):
        return self.title