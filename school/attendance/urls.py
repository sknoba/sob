from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
      path('', AttendanceDashboadView.as_view(), name='attendance-dashboard'),
      path('classes/', AttendanceClassList.as_view(), name='att-class-list'),
      path('<int:class_id>/previous-records/', AttendanceLogView.as_view(), name='attendance-log'),
      path('<int:class_id>/class-attendance', ClassAttendanceView.as_view(), name='class-attendance'),
      path('<int:class_id>/mark-attendance', MarkAttendanceView.as_view(), name='mark-attendance'),


      # path('<int:pk>/stu-attendance/', StudentAttendanceListView.as_view(), name='stu-attendance-list'),
      # path('<int:pk>/stu-attendance2/', StudentAttendanceList2.as_view(), name='stu-attendance-list'),
      # # path('<int:pk>/mark-attendance/', AttendanceList.as_view(), name='mark-attendance'),
      # # path('<int:pk>/<int:clsi>/delete/', AttendanceDeleteView.as_view(), name='delete-attendance'),
      # path('attendance/', index, name='attendance'),
      
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)