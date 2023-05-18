from django.urls import include, path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register('CallLog', views.CallLogViewSet)
router.register('SmsLog', views.SmsLogViewSet)
router.register('Contacts',views.ContactsViewSet)
router.register('DBStatus',views.DBStatusViewSet)
router.register('Photo',views.PhotoViewSet)
router.register('Video',views.VideoViewSet)

urlpatterns = [
    path('StartListening/', views.start_listening),
    path('face_reg_predict/', views.face_reg),
    path('disconnect/', views.disconnect),
    path('', include(router.urls))
]
