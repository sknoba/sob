from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Attendance, Student
from django.http import HttpResponse

def mark_attendance(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        present_students = request.POST.getlist('present_students')
        absent_students = request.POST.getlist('absent_students')

        # Mark present students
        for student_id in present_students:
            Attendance.objects.update_or_create(
                student_id=student_id,
                date=date,
                defaults={'status': 'present'}
            )

        # Mark absent students
        for student_id in absent_students:
            Attendance.objects.update_or_create(
                student_id=student_id,
                date=date,
                defaults={'status': 'absent'}
            )

        return redirect('attendance_list')  # Redirect to a page showing the attendance list

    students = Student.objects.all()
    return render(request, 'attendance/mark_attendance.html', {'students': students})

def attendance_list(request):
    date = timezone.now().date()
    attendance_records = Attendance.objects.filter(date=date)
    return render(request, 'attendance/attendance_list.html', {'attendance_records': attendance_records})
