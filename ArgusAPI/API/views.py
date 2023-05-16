from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import CallLog,SmsLog,Contacts
from .serializers import CallLogSerializer,SmsLogSerializer,ContactsSerializer
from .filters import SmsLogFilter, CallLogFilter, ContactsFilter

@api_view(['POST'])
def start_listerning(request):

    return Response("Working")


@api_view()
def status(request):
    return Response("Current Status")

@api_view(['POST'])
def face_reg(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']

        # Generate a unique filename
        filename = os.path.join(settings.MEDIA_ROOT, 'facereg/predict', image.name)

        # Save the image to a temporary location
        with open(filename, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)
    return Response("Current Status")

class CallLogViewSet(ReadOnlyModelViewSet):
    queryset = CallLog.objects.all()
    serializer_class = CallLogSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = CallLogFilter
    ordering_fields = ['datetime','duration']

class SmsLogViewSet(ReadOnlyModelViewSet):
    queryset = SmsLog.objects.all()
    serializer_class = SmsLogSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_class = SmsLogFilter
    search_fields = ['address','message']

class ContactsViewSet(ReadOnlyModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_class = ContactsFilter
    search_fields = ['name','number']
