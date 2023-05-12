from django.urls import path
from . import views


urlpatterns = [
    path('StartListening/', views.start_listerning),
    path('status/', views.status)
]
