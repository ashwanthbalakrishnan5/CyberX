import cv2
import numpy as np
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Contacts,CallLog,SmsLog,DBStatus,Photo,Video
from .serializers import ContactsSerializer,CallLogSerializer,SmsLogSerializer,DBStatusSerializer,PhotoSerializer,VideoSerializer
from .filters import ContactsFilter,CallLogFilter,SmsLogFilter
from .tasks import start_extraction
from .predict_face import predict


@api_view(['POST'])
def start_listening(request):
    start_extraction.delay()
    return Response({"start_listening":True})


@api_view(['POST'])
def face_reg(request):
    if request.method == 'POST' :
        image_file = request.FILES['image']

        # convert to required format using Numpy
        image_data = image_file.read()
        nparr = np.frombuffer(image_data, np.uint8)
        input_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        #found = predict(input_img)
        found = True

    return Response({'found': "found"})


@api_view(['POST'])
def disconnect(request):
    if request.method == 'POST' :
        tables = ['api_contacts','api_calllog', 'api_smslog','api_adbstatus','api_dbstatus','api_device','api_docs','api_photo','api_video']  
        with connection.cursor() as cursor:
            for table_name in tables:
                cursor.execute(f'TRUNCATE TABLE {table_name} RESTART IDENTITY')
        return Response({'disconnect': True})


class DBStatusViewSet(ReadOnlyModelViewSet):
    queryset = DBStatus.objects.all()
    serializer_class = DBStatusSerializer


class CallLogViewSet(ReadOnlyModelViewSet):
    queryset = CallLog.objects.prefetch_related('contacts').all()
    serializer_class = CallLogSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CallLogFilter
    ordering_fields = ['datetime', 'duration']


class SmsLogViewSet(ReadOnlyModelViewSet):
    queryset = SmsLog.objects.prefetch_related('Contacts').all()
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

class PhotoViewSet(ReadOnlyModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class VideoViewSet(ReadOnlyModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer