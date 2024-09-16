from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SearchLogViewSet

router = DefaultRouter()
router.register(r'logs', SearchLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]