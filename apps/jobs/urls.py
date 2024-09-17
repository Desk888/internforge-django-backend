from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, JobSkillViewSet
from .views import JobSearchView

router = DefaultRouter()
router.register(r'', JobViewSet)
router.register(r'skills', JobSkillViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('search/', JobSearchView.as_view(), name='job-search'),
]