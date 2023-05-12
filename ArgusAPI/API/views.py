from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def start_listerning(request):
    return Response("Working")


@api_view()
def status(request):
    return Response("Current Status")
