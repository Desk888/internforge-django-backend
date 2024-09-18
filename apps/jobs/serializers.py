from rest_framework import serializers
from apps.jobs.models import Job

class JobSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.company_name', read_only=True)
    application_count = serializers.SerializerMethodField()
    is_open = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = '__all__'

    def get_application_count(self, obj):
        return obj.application_count()

    def get_is_open(self, obj):
        return obj.is_open()