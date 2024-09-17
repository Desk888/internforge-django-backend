from rest_framework import serializers
from apps.applications.models import Application
from apps.jobs.models import Job
from django.db import IntegrityError

class ApplicationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['application_id', 'user', 'status', 'submitted_at', 'updated_at']
    
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError("You have already applied to this job.")

    def validate(self, data):
        job = data.get('job')
        if job and not job.is_open():
            raise serializers.ValidationError("This job is no longer open for applications.")
        return data