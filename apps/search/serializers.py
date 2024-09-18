from rest_framework import serializers
from apps.search.models import SearchLog

class SearchLogSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = SearchLog
        fields = ['search_log_id', 'user_email', 'query', 'searched_at', 'results_count']
        read_only_fields = ['search_log_id', 'user_email', 'searched_at']