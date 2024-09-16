from rest_framework import permissions

class IsJobSeeker(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='JOB_SEEKER').exists()

class IsEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='EMPLOYER').exists()

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='ADMIN').exists()
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
    