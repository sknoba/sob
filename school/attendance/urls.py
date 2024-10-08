from django.urls import path
from .views import mark_attendance, attendance_list

urlpatterns = [
    path('', attendance_list, name='attendance-list'),
    path('mark/', mark_attendance, name='mark-attendance'),
]