from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SkillViewSet

router = DefaultRouter()
router.register(r'', SkillViewSet)

urlpatterns = [
    path('', include(router.urls)),
]