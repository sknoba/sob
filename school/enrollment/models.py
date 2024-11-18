from django.db import models
from core.models import AcademicYear, Student, Standard
from fees.models import FeesCollection
from django.dispatch import receiver
from django.db.models.signals import post_save

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='enrollments')
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    cancel_enroll = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'academic_year')
    
    def __str__(self):
        return f'{self.student} - {self.standard} - {self.academic_year}'
    