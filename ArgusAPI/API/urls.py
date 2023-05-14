from django.urls import include, path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register('CallLog', views.CallLogViewSet)
router.register('SmsLog', views.SmsLogViewSet)

urlpatterns = [
    path('StartListening/', views.start_listerning),
    path('status/', views.status),
    path('', include(router.urls))
]
