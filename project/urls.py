from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('apps.users.urls'), name='users'),
    path('api/companies/', include('apps.companies.urls'), name='companies'),
    path('api/jobs/', include('apps.jobs.urls'), name='jobs'),
    path('api/applications/', include('apps.applications.urls'), name='applications'),
    path('api/cvs/', include('apps.cvs.urls'), name='cvs'),
    path('api/skills/', include('apps.skills.urls'), name='skills'),
    path('api/notifications/', include('apps.notifications.urls'), name='notifications'),
    path('api/search/', include('apps.search.urls'), name='search'),
]