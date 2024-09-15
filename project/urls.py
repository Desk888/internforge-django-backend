from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/companies/', include('apps.companies.urls')),
    path('api/jobs/', include('apps.jobs.urls')),
    path('api/applications/', include('apps.applications.urls')),
    path('api/cvs/', include('apps.cvs.urls')),
    path('api/skills/', include('apps.skills.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/search/', include('apps.search.urls')),
]