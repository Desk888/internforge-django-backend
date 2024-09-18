from django_filters import rest_framework as filters
from .models import Application
from .constants import APPLICATION_STATUS

class ApplicationFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=APPLICATION_STATUS)
    submitted_after = filters.DateFilter(field_name="submitted_at", lookup_expr='gte')
    submitted_before = filters.DateFilter(field_name="submitted_at", lookup_expr='lte')

    class Meta:
        model = Application
        fields = ['status', 'submitted_after', 'submitted_before']