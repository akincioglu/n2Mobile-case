from django.urls import path, include
from rest_framework.routers import SimpleRouter
from ..views.user import UserViewSet

router = SimpleRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = router.urls