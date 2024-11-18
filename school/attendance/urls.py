from django.urls import path
from . import views
from . views import StudentAttendanceListView, AttendanceClassList, AttendanceList, AttendanceDashboadView, AttendanceDeleteView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', AttendanceDashboadView.as_view(), name='attendance-dashboard'),
    path('<int:pk>/mark-attendance/', AttendanceList.as_view(), name='mark-attendance'),
    path('<int:pk>/<int:clsi>/delete/', AttendanceDeleteView.as_view(), name='delete-attendance'),
    path('<int:pk>/stu-attendance/', StudentAttendanceListView.as_view(), name='stu-attendance-list'),
    path('cls-att-list/', AttendanceClassList.as_view(), name='cls-att-list'),
    # path('log/', views.log, name='log'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)