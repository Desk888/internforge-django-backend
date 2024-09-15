from django.db import models
from apps.users.models import User

class SearchLog(models.Model):
    search_log_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=100)
    searched_at = models.DateTimeField()

    def __str__(self):
        return f'SearchLog {self.search_log_id}'