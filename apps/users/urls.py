from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, UserSkillViewSet, UserCreateView,
    VerifyEmailView, PasswordResetView, SetNewPasswordView
    )

router = DefaultRouter()
router.register(r'', UserViewSet)
router.register(r'skills', UserSkillViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password-reset-confirm/', SetNewPasswordView.as_view(), name='set-new-password'),
]