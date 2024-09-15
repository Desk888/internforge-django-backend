from rest_framework import serializers
from apps.cvs.models import CV

class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = '__all__'