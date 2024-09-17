from rest_framework import permissions

class IsOwnerOrEmployerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if request.user.user_type == 'JOB_SEEKER':
            return obj.user == request.user
        if request.user.user_type == 'EMPLOYER':
            return obj.job.company.user == request.user
        return False