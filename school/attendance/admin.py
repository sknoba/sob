from django.contrib import admin
from .models import Attendance, MarkAttendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('standard', 'datetime', 'present_boy', 'present_girl','teacher')    

@admin.register(MarkAttendance)
class MarkAttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'status','attendance')
    search_fields = ('status',)

