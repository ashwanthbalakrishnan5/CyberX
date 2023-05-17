import cv2
import numpy as np
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import CallLog, SmsLog, Contacts
from .serializers import CallLogSerializer, SmsLogSerializer, ContactsSerializer
from .filters import SmsLogFilter, CallLogFilter, ContactsFilter
from .tasks import test_cel
from .predict_face import predict


@api_view(['POST'])
def start_listerning(request):
    test_cel.delay("start")
    return Response("Running")


@api_view()
def status(request):
    return Response("Current Status")


@api_view(['POST'])
def face_reg(request):
    if request.method == 'POST' :
        image_file = request.FILES['image']

        # convert to required format using Numpy
        image_data = image_file.read()
        nparr = np.frombuffer(image_data, np.uint8)
        input_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        found = predict(input_img)

    return Response({'found': found})


class CallLogViewSet(ReadOnlyModelViewSet):
    queryset = CallLog.objects.all()
    serializer_class = CallLogSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CallLogFilter
    ordering_fields = ['datetime', 'duration']


class SmsLogViewSet(ReadOnlyModelViewSet):
    queryset = SmsLog.objects.all()
    serializer_class = SmsLogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = SmsLogFilter
    search_fields = ['address', 'message']


class ContactsViewSet(ReadOnlyModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ContactsFilter
    search_fields = ['name', 'number']
