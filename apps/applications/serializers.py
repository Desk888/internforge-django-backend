from rest_framework import serializers
from apps.applications.models import Application
from apps.cvs.models import CV
from apps.jobs.models import Job

class ApplicationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    cv = serializers.PrimaryKeyRelatedField(queryset=CV.objects.all(), required=False)
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())
    job_title = serializers.CharField(source='job.title', read_only=True)
    company_name = serializers.CharField(source='job.company.name', read_only=True)
    
    class Meta:
        model = Application
        fields = ['application_id', 'job', 'job_title', 'company_name', 'user', 'cv', 'cover_letter', 'status', 'submitted_at']
        read_only_fields = ['application_id', 'user', 'status', 'submitted_at']
    
    def validate_cv(self, value):
        if value and value.user != self.context['request'].user:
            raise serializers.ValidationError("You can only use your own CV.")
        return value

    def validate_job(self, value):
        if not value.is_open():
            raise serializers.ValidationError("This job is no longer open for applications.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        if 'cv' not in validated_data:
            active_cv = CV.objects.filter(user=user, is_active=True).first()
            if active_cv:
                validated_data['cv'] = active_cv
            else:
                raise serializers.ValidationError("No active CV found. Please upload a CV before applying.")
        
        validated_data['user'] = user
        validated_data['status'] = 'PENDING'
        
        return super().create(validated_data)

    def validate(self, data):
        user = self.context['request'].user
        job = data.get('job')
        if job and Application.objects.filter(user=user, job=job).exists():
            raise serializers.ValidationError("You have already applied to this job.")
        return data