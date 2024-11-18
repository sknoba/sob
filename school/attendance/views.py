from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Attendance, MarkAttendance
from core.models import Student, Standard
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.base import View
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse

class AttendanceDashboadView(ListView):
    model = Attendance
    template_name = 'attendance/dashboard.html'
    context_object_name = 'attendance'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_standard'] = Standard.objects.all().count()
        context['total_students'] = Student.objects.all().count()
        context['total_attendance'] = Attendance.objects.all().count()
        return context

class AttendanceClassList(ListView):
    model = Standard
    template_name = 'attendance/classes_list.html'
    context_object_name = 'standards'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_standard'] = Standard.objects.all().count()
        return context

class AttendanceList(ListView):
    model = Attendance
    template_name = 'attendance/mark_attendance.html'
    context_object_name = 'attendance'
    url_kwarg = 'pk'

    # def get_queryset(self):
    #     attendance = Attendance.objects.filter(standard_id=self.kwargs.get('pk'))
    #     if attendance.filter(datetime__date=timezone.datetime.now().date()).exists():
    #         if self.request.GET.get('date'):
    #             attendance = attendance.get(datetime__date=self.request.GET.get('date'))
    #         else:
    #             attendance = attendance.get(datetime__date=timezone.datetime.now().date())
    #     else:
    #         attendance.none()        
    #     return attendance

    def get_queryset(self):
        attendance = Attendance.objects.filter(standard_id=self.kwargs.get('pk'))
        if self.request.GET.get('date'):
            if attendance.filter(datetime__date=self.request.GET.get('date')).exists():
                attendance = attendance.get(datetime__date=self.request.GET.get('date'))
            else:
                pass
        else:
            if attendance.filter(datetime__date=timezone.datetime.now().date()).exists():
               attendance =  attendance.get(datetime__date=timezone.datetime.now().date())
            else:
                attendance = attendance.none()
        return attendance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        standard = Standard.objects.get(id=self.kwargs.get('pk'))
        today = timezone.datetime.now().date()
        context['today']= today
        context['today_attendance']=  Attendance.objects.filter(standard_id=self.kwargs.get('pk'),datetime__date=today)
        context['standard'] = standard
        # context['total_students'] = standard.student_set.all().count()
        return context


class AttendanceDeleteView(DeleteView):
    model = Attendance    

    def post(self, request, *args, **kwargs):
        clsi_value = self.kwargs.get('clsi')
        print(clsi_value)
        self.object = self.get_object()  # Get the object to delete
        self.object.delete()  # Delete the object
        return redirect('mark-attendance', pk=self.kwargs.get('clsi'))

def update_present_counts(attendance):
        present_boys = attendance.attendance.filter(status=True, student__gender='male').count()
        present_girls = attendance.attendance.filter(status=True, student__gender='female').count()
        attendance.present_boy = present_boys
        attendance.present_girl = present_girls
        attendance.save()

class StudentAttendanceListView(ListView):
    model = Student
    template_name = 'attendance/attendance_record.html'
    context_object_name = 'students'
    url_kwarg = 'pk'
    
    def get_queryset(self):
        standard = get_object_or_404(Standard, id=self.kwargs.get('pk'))
        return Student.objects.filter(standard=standard)

    def post(self, request, *args, **kwargs):
        attendance_record = []
        today = timezone.datetime.now().date()
        teacher = Standard.objects.get(id=self.kwargs.get('pk')).class_teacher
        if not Attendance.objects.filter(standard_id=self.kwargs.get('pk'), datetime__date=today).exists():
            attendance = Attendance.objects.create(standard_id=self.kwargs.get('pk'),teacher=teacher, datetime=today)
        else:
            attendance = Attendance.objects.get(standard_id=self.kwargs.get('pk'), datetime__date=today)
        
        mark_attendance = MarkAttendance.objects.filter(attendance=attendance)
        for student in self.get_queryset():
            status = f'{student.id}' in request.POST
            if mark_attendance.filter(student=student).exists():
                mark_attendance.filter(student=student).update(status=status)
            else:
                attendance_record.append(MarkAttendance(attendance=attendance, student=student, status=status))
        MarkAttendance.objects.bulk_create(attendance_record, ignore_conflicts=True)
        update_present_counts(attendance)
        return redirect('mark-attendance', pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['total_students'] = Student.objects.all().count()
        # context['standard'] = Standard.objects.get(id=self.kwargs.get('pk'))
        context['date']= timezone.now()
        return context
    

