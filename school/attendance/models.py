from django.db import models
from core.models import Student 
from django.utils import timezone

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student} - {self.date}: {self.status}"