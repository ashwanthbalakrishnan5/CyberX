import django_filters
from django_filters import rest_framework as filters
from datetime import datetime

from .models import SmsLog, CallLog ,Contacts

class SmsLogFilter(filters.FilterSet):
    def filter_specific_number(self, queryset, name, value):
        if value:
            numbers = queryset.order_by('address').values_list('address', flat=True).distinct()
            filtered_queryset = queryset.none()
            for number in numbers:
                row = queryset.filter(address=number).first()
                if row:
                    filtered_queryset |= queryset.filter(id=row.id)
            return filtered_queryset
        return queryset
    def filter_is_international(self, queryset, name, value):
        if value:
            return queryset.exclude(number__startswith='+91')
        else:
            return queryset.filter(number__startswith='+91')
    is_international = django_filters.BooleanFilter(
        method='filter_is_international'
    )

    unique_number = django_filters.BooleanFilter(method='filter_specific_number')

    is_known = django_filters.BooleanFilter(
        field_name='contacts', lookup_expr='isnull', exclude=True
    )
    start_date = django_filters.IsoDateTimeFilter(
        field_name='datetime', lookup_expr='gte'
    )
    end_date = django_filters.IsoDateTimeFilter(
        field_name='datetime', lookup_expr='lte'
    )
    class Meta:
        model = SmsLog
        fields = ['start_date', 'end_date', 'sms_type','is_known','is_international','address','unique_number']

class CallLogFilter(filters.FilterSet):
    # def filter_specific_number(self, queryset, name, value):
    #     if value:
    #         numbers = queryset.order_by('number').values_list('number', flat=True).distinct()
    #         filtered_queryset = queryset.none()
    #         for number in numbers:
    #             row = queryset.filter(number=number).first()
    #             if row:
    #                 filtered_queryset |= queryset.filter(id=row.id)
    #         return filtered_queryset
    #     return queryset

    #unique_number = django_filters.BooleanFilter(method='filter_specific_number')
    def filter_is_international(self, queryset, name, value):
        if value:
            return queryset.exclude(number__startswith='+91')
        else:
            return queryset.filter(number__startswith='+91')

    is_international = django_filters.BooleanFilter(
        method='filter_is_international'
    )


    start_date = django_filters.IsoDateTimeFilter(
        field_name='datetime', lookup_expr='gte'
    )
    end_date = django_filters.IsoDateTimeFilter(
        field_name='datetime', lookup_expr='lte'
    )
    is_known = django_filters.BooleanFilter(
        field_name='contacts', lookup_expr='isnull', exclude=True
    )
    class Meta:
        model = CallLog
        fields = ['start_date', 'end_date','is_known','is_international','call_type','number']


class ContactsFilter(filters.FilterSet):
    class Meta:
        model = Contacts
        fields = []
        
        