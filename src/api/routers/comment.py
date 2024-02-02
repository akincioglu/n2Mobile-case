from django.urls import path, include
from rest_framework.routers import SimpleRouter
from ..views.comment import CommentViewSet

router = SimpleRouter()
router.register(r'', CommentViewSet, basename='user')

urlpatterns = router.urls