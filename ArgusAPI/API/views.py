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
from .models import Contacts,CallLog,SmsLog,DBStatus,Photo,Video,ADBStatus,Device
from .serializers import ContactsSerializer,CallLogSerializer,SmsLogSerializer,DBStatusSerializer,PhotoSerializer,VideoSerializer,ADBStatusSerializer,DeviceSerializer
from .filters import ContactsFilter,CallLogFilter,SmsLogFilter
from .tasks import start_extraction
from .predict_face import predict


@api_view(['GET','POST'])
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
        tables = ['API_calllog', 'API_smslog','API_contacts','API_adbstatus','API_dbstatus','API_device','API_docs','API_photo','API_video']  
        with connection.cursor() as cursor:
            cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
            for table_name in tables:
                cursor.execute(f'TRUNCATE TABLE {table_name}')
            cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')
        return Response({'disconnect': True})

class ADBStatusViewSet(ReadOnlyModelViewSet):
    queryset = ADBStatus.objects.all()
    serializer_class = ADBStatusSerializer

class DeviceViewSet(ReadOnlyModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
class DBStatusViewSet(ReadOnlyModelViewSet):
    queryset = DBStatus.objects.all()
    serializer_class = DBStatusSerializer


class CallLogViewSet(ReadOnlyModelViewSet):
    queryset = CallLog.objects.all()
    serializer_class = CallLogSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CallLogFilter
    ordering_fields = ['datetime', 'duration']


class SmsLogViewSet(ReadOnlyModelViewSet):
    queryset = SmsLog.objects.prefetch_related('Contacts').all()
    serializer_class = SmsLogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = SmsLogFilter
    search_fields = ['message']


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

# class ConnectionMethodViewSet(Read)