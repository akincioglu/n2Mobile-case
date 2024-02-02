from django.urls import path, include
from rest_framework.routers import SimpleRouter
from ..views.post import PostViewSet

router = SimpleRouter()
router.register(r'', PostViewSet, basename='user')

urlpatterns = router.urls