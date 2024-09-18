from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    notification_type_display = serializers.CharField(source='get_notification_type_display', read_only=True)
    related_object = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'user', 'notification_type', 'notification_type_display', 'message', 
                  'related_object_id', 'related_object_type', 'is_read', 'created_at', 'related_object']
        read_only_fields = ['id', 'user', 'notification_type', 'notification_type_display', 
                            'message', 'related_object_id', 'related_object_type', 'created_at']
                            
    def get_related_object(self, obj):
        if obj.content_object:
            return {
                'type': obj.content_object._meta.model_name,
                'id': obj.object_id,
                'str': str(obj.content_object)
            }
        return None