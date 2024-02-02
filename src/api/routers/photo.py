from django.urls import path, include
from rest_framework.routers import SimpleRouter
from ..views.photo import PhotoViewSet

router = SimpleRouter()
router.register(r'', PhotoViewSet, basename='user')

urlpatterns = router.urls