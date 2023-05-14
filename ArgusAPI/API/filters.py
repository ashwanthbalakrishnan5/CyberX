import django_filters
from django_filters import rest_framework as filters
from datetime import datetime

from .models import SmsLog

class SmsLogFilter(filters.FilterSet):
    start_date = django_filters.IsoDateTimeFilter(
        field_name='datetime', lookup_expr='gte'
    )
    end_date = django_filters.IsoDateTimeFilter(
        field_name='datetime', lookup_expr='lte'
    )
    class Meta:
        model = SmsLog
        fields = ['start_date', 'end_date', 'sms_type']
