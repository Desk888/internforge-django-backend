from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SearchLogViewSet, PerformSearchView  # Assuming we add a PerformSearchView

router = DefaultRouter()
router.register(r'search-logs', SearchLogViewSet, basename='search-log')

urlpatterns = [
    path('', include(router.urls)),
    path('perform-search/', PerformSearchView.as_view(), name='perform-search'),
]