from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    notification_type_display = serializers.CharField(source='get_notification_type_display', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'user', 'notification_type', 'notification_type_display', 'message', 
                  'related_object_id', 'related_object_type', 'is_read', 'created_at']
        read_only_fields = ['id', 'user', 'notification_type', 'notification_type_display', 
                            'message', 'related_object_id', 'related_object_type', 'created_at']