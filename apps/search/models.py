from django.db import models
from apps.users.models import User
from django.conf import settings

class SearchLog(models.Model):
    search_log_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='search_logs')
    query = models.CharField(max_length=255)
    searched_at = models.DateTimeField(auto_now_add=True)
    results_count = models.IntegerField()

    def __str__(self):
        return f"{self.user.email}'s search: {self.query}"