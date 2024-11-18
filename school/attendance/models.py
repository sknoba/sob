from django.db import models
from django.core.exceptions import ValidationError
from core.models import Student, UserProfile, Standard
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.db.models import UniqueConstraint
from django.db.models import F

class Attendance(models.Model):
    datetime = models.DateTimeField(auto_now=False)
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='attendance_teacher')
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name='attendance_standard')
    present_boy = models.PositiveIntegerField(default=0, editable=False)
    present_girl = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['standard', 'datetime'],
                name='unique_attendance_per_day'
            )
        ]
    def clean(self):
        # Ensure no duplicates for the same day
        if Attendance.objects.filter(
            standard=self.standard, 
            datetime__date=self.datetime.date()
        ).exclude(id=self.id).exists():
            raise ValidationError("Attendance for this teacher and standard already exists for today.")

    def __str__(self):
        return f"{self.standard} - {self.datetime}: {self.teacher.first_name} {self.teacher.last_name}"
    

class MarkAttendance(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='attendance')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student')
    status = models.BooleanField(default=False)

    class Meta:
       constraints = [
            UniqueConstraint(fields=['attendance', 'student'], name='unique_student_per_attendance')
        ]


    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name}  - {self.attendance.datetime} - {self.status}"
   
