from django.urls import path
from .import views
from .views import StudentAttendanceListView, AttendanceClassList
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('classes/', AttendanceClassList.as_view(), name='attendance-list'),
    path('', StudentAttendanceListView.as_view(), name='attendance-list'),
    path('log/', views.log, name='log'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)