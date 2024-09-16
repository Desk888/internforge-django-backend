from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserSkillViewSet, UserCreateView

router = DefaultRouter()
router.register(r'', UserViewSet)
router.register(r'skills', UserSkillViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserCreateView.as_view(), name='user-register'),
]