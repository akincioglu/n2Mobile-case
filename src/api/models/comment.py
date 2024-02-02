from django.db import models
from .user import User
from .post import Post

class Comment(models.Model):
    postId = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()

    def __str__(self):
        return f"Comment by {self.userName} on Post {self.postId}"