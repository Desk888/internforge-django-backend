from django.urls import path
from .views import JobSeekerDashboardView, EmployerDashboardView, AdminDashboardView

urlpatterns = [
    path('job-seeker/', JobSeekerDashboardView.as_view(), name='job-seeker-dashboard'),
    path('employer/', EmployerDashboardView.as_view(), name='employer-dashboard'),
    path('admin/', AdminDashboardView.as_view(), name='admin-dashboard'),
]