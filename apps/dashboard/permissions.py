from rest_framework import permissions

class IsEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'EMPLOYER'

class IsJobSeeker(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'JOB_SEEKER'