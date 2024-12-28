from django.db import models
from django.db.models import Q
from accounts.models import User
from student.models import Student
from core.models import Class
from simple_history.models import HistoricalRecords
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver


# class Attendance(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
#     date =  models.DateTimeField(auto_now=True)
#     status = models.CharField(
#         max_length=10,
#         choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')]
#     )
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_attendance')

#     class Meta:
#         unique_together = ('student', 'date')

#     def __str__(self):
#         return f"{self.student} - {self.date} - {self.status}"

from django.utils.timezone import localdate
from django.core.exceptions import ValidationError

class Attendance(models.Model):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='attendance', verbose_name='Class')
    date =  models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_attendance', limit_choices_to={'user_type__in': ['T','P']}, verbose_name="Created By")
    present = models.IntegerField(default=0)
    absent = models.IntegerField(default=0)
    history = HistoricalRecords()

    class Meta:
            constraints = [
                models.UniqueConstraint(fields=['class_name', 'date'], name='unique_attendance_per_class_per_date')
            ]

    def clean(self):
            # Check if an Attendance record for this class and date already exists
        today = localdate(self.date)
        if Attendance.objects.filter(class_name=self.class_name, date__date=today).exists():
            raise ValidationError(f"Attendance for {self.class_name} on {today} already exists.")
        super().clean()

    def __str__(self):
        return f"{self.class_name} - {self.created_by} - {self.date.date().strftime('%d %b, %y')} - {self.date.time().strftime('%I:%M %p')}"


class AttendaceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='attendance_records')
    status = models.BooleanField()
    history = HistoricalRecords()

    class Meta:
        unique_together = ('student', 'attendance')

    def __str__(self):
        return f"{self.attendance}- {self.student} - {self.status} "
    


# def update_attendance_counts(attendance):
#     """
#     Helper function to recalculate attendance counts for a specific class attendance.
#     """
#     total_present = attendance.attendance.filter(status='Present').count()
#     total_absent = attendance.attendance.filter(status='Absent').count()

#     attendance.present = total_present
#     attendance.absent = total_absent
#     attendance.save()

# @receiver(post_save, sender=AttendaceRecord)
# def handle_attendance_record_save(sender, instance, created, **kwargs):
#     """
#     Triggered when an attendance record is created or updated.
#     """
#     attendance = instance.attendance
#     update_attendance_counts(attendance)


# def update_attendance_counts(attendance):
#     counts = attendance.attendance.aggregate(
#         total_present=Count('id', filter=Q(status='Present')),
#         total_absent=Count('id', filter=Q(status='Absent'))
#     )
#     attendance.present = counts['total_present']
#     attendance.absent = counts['total_absent']
#     attendance.save()