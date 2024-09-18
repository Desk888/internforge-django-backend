from django_filters import rest_framework as filters
from .models import Company

class CompanyFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    industry = filters.CharFilter(lookup_expr='icontains')
    min_employees = filters.NumberFilter(field_name="employee_count", lookup_expr='gte')
    max_employees = filters.NumberFilter(field_name="employee_count", lookup_expr='lte')
    founded_after = filters.NumberFilter(field_name="founded_year", lookup_expr='gte')
    founded_before = filters.NumberFilter(field_name="founded_year", lookup_expr='lte')

    class Meta:
        model = Company
        fields = ['name', 'industry', 'min_employees', 'max_employees', 'founded_after', 'founded_before']