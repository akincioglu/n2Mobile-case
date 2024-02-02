from django.urls import path, include
from .routers import user, post, album, todo, comment, photo

urlpatterns = [
    path('users/', include(user.urls)),
    path('users/<int:userId>/posts/', include(post.urls)),
    path('users/<int:userId>/albums/', include(album.urls)),
    path('users/<int:userId>/todos/', include(todo.urls)),
    path('posts/<int:postId>/comments/', include(comment.urls)),
    path('albums/<int:albumId>/photos/', include(photo.urls))
]