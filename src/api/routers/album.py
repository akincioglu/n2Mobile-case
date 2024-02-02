from django.urls import path, include
from rest_framework.routers import SimpleRouter
from ..views.album import AlbumViewSet

router = SimpleRouter()
router.register(r'', AlbumViewSet, basename='user')

urlpatterns = router.urls