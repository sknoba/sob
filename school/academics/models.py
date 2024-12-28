from django.db import models
from core.models import Class, Subject, AcademicYear
from student.models import Enrollment
from simple_history.models import HistoricalRecords
from core.models import Subject
from accounts.models import User

EXAM= (
    ('p1', 'Periodic Test 1'),
    ('p2', 'Periodic Test 2'),
    ('t1', 'Term Examination 1'),
    ('t2', 'Term Examination 2'),
)

class Exams(models.Model):
    exam = models.CharField(max_length=10 ,choices=EXAM)    
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    result_date = models.DateField()
    note = models.TextField(null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        unique_together = ['exam', 'class_name', 'academic_year']

    def __str__(self):
        return self.exam


class ExamScore(models.Model):
    exam = models.ForeignKey(Exams, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(Enrollment, on_delete=models.CASCADE)    
    theory_marks = models.FloatField()
    slip_test_marks = models.FloatField()
    seminar_marks = models.FloatField()
    note_book_keeping_marks = models.FloatField()
    subject_enrichment = models.FloatField()
    note = models.TextField(null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.exam.exam + ' - ' + self.subject.name + ' - ' + self.student.student.first_name


class TimeTable(models.Model):
    exam = models.ForeignKey(Exams, on_delete=models.CASCADE, related_name='titmetable')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subjecttimetable')
    date = models.DateTimeField()
    duration = models.DurationField()
    info = models.TextField(null=True, blank=True)
    history = HistoricalRecords()    

    def __str__(self):
        return self.exam.exam + ' - ' + self.subject.name + ' - ' + str(self.date)
    

class TeacherTest(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    taken_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher', limit_choices_to={'user_type': 'T'}, verbose_name="Cunduct By")
    subjects = models.ForeignKey(Subject, on_delete=models.CASCADE)
    duration = models.DurationField()
    total_marks = models.PositiveIntegerField()
    info = models.TextField(null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name + ' - ' + self.class_name.name + ' - ' + self.subject.name


class TestScoring(models.Model):
    test = models.ForeignKey(TeacherTest, on_delete=models.CASCADE)
    student = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    obtain_mark = models.FloatField()
    result = models.CharField(max_length=10, choices=(('p', 'Pass'), ('f', 'Fail')))
    history = HistoricalRecords()

    def __str__(self):
        return self.test.name + ' - ' + self.student.student.first_name