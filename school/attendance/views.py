from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.timezone import now
from .models import Attendance, AttendaceRecord
from core.models import Class, AcademicYear
from student.models import Student, Enrollment
# from django.http import HttpResponse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views import View
# from django.views.generic.base import View
# from django.http import JsonResponse
# from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from datetime import date
# from django.urls import reverse_lazy, reverse
# from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

class AttendanceDashboadView(ListView):
    model = Attendance
    template_name = 'attendance/dashboard.html'
    context_object_name = 'attendance'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_standard'] = Class.objects.all().count()
        context['total_students'] = Student.objects.all().count()
        context['total_attendance'] = Attendance.objects.all().count()
        return context

class AttendanceClassList(ListView):
    model = Class
    template_name = 'attendance/classes_list.html'
    context_object_name = 'classes'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_standard'] = Class.objects.all().count()
        return context

class AttendanceLogView(ListView):
    model = Attendance
    template_name = 'attendance/attendance_log.html'
    context_object_name = 'attendance'
    url_kwarg = 'class_id'


class ClassAttendanceView(ListView):
    model = Attendance
    template_name = 'attendance/class_attendance.html'
    context_object_name = 'attendance'
    url_kwarg = 'class_id'

    def get_queryset(self):
        attendance = Attendance.objects.filter(class_name_id=self.kwargs.get('class_id'), date__date=timezone.datetime.now().date())
        if attendance.exists():
            return attendance
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['class'] = Class.objects.get(id=self.kwargs.get('class_id'))
        return context
    

class MarkAttendanceView(ListView):
    model = Enrollment
    template_name = 'attendance/mark_attendance.html'
    context_object_name = 'students'
    url_kwarg = 'class_id'
   

    def get_queryset(self):
        current_ay = AcademicYear.objects.get(start_date__lte=date.today(), end_date__gte=date.today())
        students = Enrollment.objects.filter(academic_year=current_ay, standard_id=self.kwargs.get('class_id'))
        return students


    def post(self, request, *args, **kwargs):
        attendance_record = []
        class_id = self.kwargs.get('class_id')
        attendance = Attendance.objects.filter(class_name_id=class_id, date__date=date.today())
        if attendance.exists():
            attendance = attendance.first()
        else:
            attendance = attendance.create(class_name_id=class_id, 
                        date=now(), 
                        created_by=request.user)

        attendance_record = AttendaceRecord.objects.filter(attendance=attendance)
        
        for student in self.get_queryset():
            status = f'{student.student.id}' in request.POST   
            record = attendance_record.filter(student=student.student).first()
            if record:
                # Update and save to trigger historical record
                record.status = status
                record.save()
                send_push_notification(
                        user=student.student.user,
                        title="Attendance Updated",
                        body=f"Your attendance was updated by {request.user.username}.",
                        url="/attendance/"
                    )
            else:
                # Create a new record, which automatically triggers historical record
                AttendaceRecord.objects.create(
                    student=student.student,
                    attendance=attendance,
                    status=status
                )    
                send_push_notification(
                        user=student.student.user,
                        title="Attendance Created",
                        body=f"Your attendance was Created by {request.user.username}.",
                        url="/attendance/"
                    )
        return redirect('class-attendance', class_id=self.kwargs.get('class_id'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['class'] = Class.objects.get(id=self.kwargs.get('class_id'))
        return context
       



import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pywebpush import webpush, WebPushException
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from accounts.models import WebPushSubscription
from django.conf import settings
from core.views import send_push_notification



# # class AttendanceList(ListView):
# #     model = Attendance
# #     template_name = 'attendance/mark_attendance.html'
# #     context_object_name = 'attendance'
# #     url_kwarg = 'pk'

# #     # def get_queryset(self):
# #     #     attendance = Attendance.objects.filter(standard_id=self.kwargs.get('pk'))
# #     #     if attendance.filter(datetime__date=timezone.datetime.now().date()).exists():
# #     #         if self.request.GET.get('date'):
# #     #             attendance = attendance.get(datetime__date=self.request.GET.get('date'))
# #     #         else:
# #     #             attendance = attendance.get(datetime__date=timezone.datetime.now().date())
# #     #     else:
# #     #         attendance.none()        
# #     #     return attendance

# #     def get_queryset(self):
# #         attendance = Attendance.objects.filter(standard_id=self.kwargs.get('pk'))
# #         if self.request.GET.get('date'):
# #             if attendance.filter(datetime__date=self.request.GET.get('date')).exists():
# #                 attendance = attendance.get(datetime__date=self.request.GET.get('date'))
# #             else:
# #                 pass
# #         else:
# #             if attendance.filter(datetime__date=timezone.datetime.now().date()).exists():
# #                attendance =  attendance.get(datetime__date=timezone.datetime.now().date())
# #             else:
# #                 attendance = attendance.none()
# #         return attendance

# #     def get_context_data(self, **kwargs):
# #         context = super().get_context_data(**kwargs)
# #         standard = Class.objects.get(id=self.kwargs.get('pk'))
# #         today = timezone.datetime.now().date()
# #         context['today']= today
# #         context['today_attendance']=  Attendance.objects.filter(standard_id=self.kwargs.get('pk'),datetime__date=today)
# #         context['standard'] = standard
# #         # context['total_students'] = standard.student_set.all().count()
# #         return context

# class AttendanceList(ListView):
#     pass





# class AttendanceDeleteView(DeleteView):
#     model = Attendance    

#     def post(self, request, *args, **kwargs):
#         clsi_value = self.kwargs.get('clsi')
#         print(clsi_value)
#         self.object = self.get_object()  # Get the object to delete
#         self.object.delete()  # Delete the object
#         return redirect('mark-attendance', pk=self.kwargs.get('clsi'))

# def update_present_counts(attendance):
#         present_boys = attendance.attendance.filter(status=True, student__gender='male').count()
#         present_girls = attendance.attendance.filter(status=True, student__gender='female').count()
#         attendance.present_boy = present_boys
#         attendance.present_girl = present_girls
#         attendance.save()

# class StudentAttendanceListView(ListView):
#     model = Student
#     template_name = 'attendance/attendance.html'
#     context_object_name = 'students'
#     url_kwarg = 'pk'
    
#     def get_queryset(self):
#         standard = get_object_or_404(Class, id=self.kwargs.get('pk'))
#         return Student.objects.all()

#     def post(self, request, *args, **kwargs):
#         attendance_record = []
#         today = timezone.datetime.now().date()
#         teacher = Class.objects.get(id=self.kwargs.get('pk')).class_teacher
#         if not Attendance.objects.filter(standard_id=self.kwargs.get('pk'), datetime__date=today).exists():
#             attendance = Attendance.objects.create(standard_id=self.kwargs.get('pk'),teacher=teacher, datetime=today)
#         else:
#             attendance = Attendance.objects.get(standard_id=self.kwargs.get('pk'), datetime__date=today)
        
#         # mark_attendance = MarkAttendance.objects.filter(attendance=attendance)
#         # for student in self.get_queryset():
#         #     status = f'{student.id}' in request.POST
#         #     if mark_attendance.filter(student=student).exists():
#         #         mark_attendance.filter(student=student).update(status=status)
#         #     else:
#         #         attendance_record.append(MarkAttendance(attendance=attendance, student=student, status=status))
#         # MarkAttendance.objects.bulk_create(attendance_record, ignore_conflicts=True)
#         # update_present_counts(attendance)
#         # return redirect('mark-attendance', pk=self.kwargs.get('pk'))

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['total_students'] = Student.objects.all().count()
#         context['standard'] = Class.objects.get(id=self.kwargs.get('pk'))
#         context['date']= timezone.now()
#         return context
    

# from student.models import Enrollment

# class StudentAttendanceList2(ListView):
#     model = Enrollment
#     template_name = 'attendance/attendance2.html'
#     context_object_name = 'students'
#     url_kwarg = 'pk'





