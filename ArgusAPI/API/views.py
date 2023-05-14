from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import CallLog,SmsLog
from .serializers import CallLogSerializer,SmsLogSerializer
from .filters import SmsLogFilter

@api_view(['POST'])
def start_listerning(request):
    return Response("Working")


@api_view()
def status(request):
    return Response("Current Status")

class CallLogViewSet(ReadOnlyModelViewSet):
    queryset = CallLog.objects.all()
    serializer_class = CallLogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['duration','call_type']

class SmsLogViewSet(ReadOnlyModelViewSet):
    queryset = SmsLog.objects.all()
    serializer_class = SmsLogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SmsLogFilter
