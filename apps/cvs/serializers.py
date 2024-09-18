from rest_framework import serializers
from apps.cvs.models import CV
from .constants import MAX_CV_SIZE

class CVSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = CV
        fields = ['cv_id', 'file_name', 'file_path', 'file_url', 'uploaded_at', 'is_active']
        read_only_fields = ['cv_id', 'uploaded_at', 'file_url']

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file_path and hasattr(obj.file_path, 'url') and request:
            return request.build_absolute_uri(obj.file_path.url)
        return None
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_file_path(self, value):
        if value.size > MAX_CV_SIZE:
            raise serializers.ValidationError(f"File size must be no more than {MAX_CV_SIZE // (1024 * 1024)} MB.")
        return value