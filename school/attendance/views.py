from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Attendance
from core.models import Student, Standard
from django.http import HttpResponse
from django.views.generic import ListView

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

class AttendanceClassList(ListView):
    model = Standard
    template_name = 'attendance/classes_list.html'
    context_object_name = 'standards'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_standard'] = Standard.objects.all().count()
        return context

class StudentAttendanceListView(ListView):
    model = Student
    template_name = 'attendance/attendance_list.html'
    context_object_name = 'students'
    
    def post(self, request, *args, **kwargs):
        print(request.POST)
        return JsonResponse({'status': 'success'})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_students'] = Student.objects.all().count()
        context['date']= timezone.now().date()
        return context
    

from django.contrib.admin.models import LogEntry
def log(request):
    logs = LogEntry.objects.all()
    return render(request, 'attendance/log.html',)