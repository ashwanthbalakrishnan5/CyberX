import django_filters
from django_filters import rest_framework as filters
from datetime import datetime

from .models import SmsLog, CallLog ,Contacts

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

class CallLogFilter(filters.FilterSet):
    def filter_is_international(self, queryset, name, value):
        if value:
            return queryset.exclude(number__startswith='+91')
        else:
            return queryset.filter(number__startswith='+91')
    start_date = django_filters.IsoDateTimeFilter(
        field_name='datetime', lookup_expr='gte'
    )
    end_date = django_filters.IsoDateTimeFilter(
        field_name='datetime', lookup_expr='lte'
    )
    is_known = django_filters.BooleanFilter(
        field_name='contacts', lookup_expr='isnull', exclude=True
    )
    is_international = django_filters.BooleanFilter(
        method='filter_is_international'
    )
    class Meta:
        model = CallLog
        fields = ['start_date', 'end_date','is_known','is_international','call_type']

class ContactsFilter(filters.FilterSet):
    class Meta:
        model = Contacts
        fields = []
        
        