from django.urls import path, include
from rest_framework.routers import SimpleRouter
from ..views.todo import TodoViewSet

router = SimpleRouter()
router.register(r'', TodoViewSet, basename='user')

urlpatterns = router.urls