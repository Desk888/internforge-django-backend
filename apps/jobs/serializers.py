from rest_framework import serializers
from apps.jobs.models import Job

class JobSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.company_name', read_only=True)
    
    class Meta:
        model = Job
        fields = '__all__'
    