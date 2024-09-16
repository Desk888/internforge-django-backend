from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, JobSkillViewSet

router = DefaultRouter()
router.register(r'', JobViewSet)
router.register(r'skills', JobSkillViewSet)

urlpatterns = [
    path('', include(router.urls)),
]