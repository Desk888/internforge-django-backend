from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserSkillViewSet

router = DefaultRouter()
router.register(r'', UserViewSet)
router.register(r'skills', UserSkillViewSet)

urlpatterns = [
    path('', include(router.urls)),
]