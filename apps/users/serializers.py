from rest_framework import serializers
from apps.users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'title', 'first_name', 'last_name', 'date_of_birth', 'email_address', 
                  'phone_number', 'address_line_one', 'address_line_two', 'city', 'country', 
                  'postcode', 'job_title', 'current_company', 'created_at', 'user_type', 
                  'is_active', 'profile_picture', 'bio']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user