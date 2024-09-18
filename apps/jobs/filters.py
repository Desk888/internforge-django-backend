from django_filters import rest_framework as filters
from .models import Job
from .constants import CONTRACT_TYPE_CHOICES, EXPERIENCE_LEVEL_CHOICES

class JobFilter(filters.FilterSet):
    min_salary = filters.NumberFilter(field_name="salary", lookup_expr='gte')
    max_salary = filters.NumberFilter(field_name="salary", lookup_expr='lte')
    company = filters.CharFilter(field_name="company__name", lookup_expr='icontains')
    location = filters.CharFilter(lookup_expr='icontains')
    job_type = filters.ChoiceFilter(choices=CONTRACT_TYPE_CHOICES)
    experience_level = filters.ChoiceFilter(choices=EXPERIENCE_LEVEL_CHOICES)

    class Meta:
        model = Job
        fields = ['company', 'location', 'job_type', 'experience_level', 'min_salary', 'max_salary']