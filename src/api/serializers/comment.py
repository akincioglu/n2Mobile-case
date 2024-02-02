from rest_framework import serializers
from ..models.comment import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'postId', 'name', "email", "body"]
