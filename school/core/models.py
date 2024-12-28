from django.db import models, transaction
from django.db.models import Max
from django.core.validators import RegexValidator
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from .utils import generate_sub_code
from django.db import models
from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from django.utils.translation import gettext_lazy as _
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
from django.utils import timezone
from simple_history.models import HistoricalRecords

class AcademicYear(models.Model):
    name = models.CharField(max_length=8, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    
    def clean(self):
        # Ensure start_date is set
        if not self.start_date:
            raise ValidationError(_("Start date is required."))
        # if self.start_date < timezone.now().date():
        #     raise ValidationError(_("Start date cannot be in the past."))
        self.end_date = self.start_date + relativedelta(years=1) - timezone.timedelta(days=1)

        if self.pk is not None:  # If this is an existing record (not a new one)
            existing_academic_year = AcademicYear.objects.get(pk=self.pk)
            if existing_academic_year.end_date < now().date():
                raise ValidationError(_("Cannot edit or change an academic year after its end date has passed."))


        # if self.is_active and self.start_date < timezone.now().date():
        #     raise ValidationError(_("Cannot set 'is_active' to True for a previous academic year."))

        start_year = self.start_date.year
        end_year = str(self.end_date.year)[-2:]  # Last two digits of the end year
        generated_name = f"{start_year}-{end_year}"

        if AcademicYear.objects.filter(name=generated_name).exists() and self.pk is None:
            raise ValidationError(
                _("The academic year with the name '%(name)s' already exists."),
                params={'name': generated_name},
            )
        self.name = generated_name

    def save(self, *args, **kwargs):
        if self.end_date and now().date() > self.end_date:
            self.is_active = False
        self.full_clean()  # Call clean() method before saving
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True, default=generate_sub_code)

    def __str__(self):
        return self.name



LETTER_CHOICES = [(chr(i), chr(i)) for i in range(ord('A'), ord('F') + 1)]

class Class(models.Model):
    name = models.CharField(max_length=50, help_text="Class 1st etc...")
    section = models.CharField(max_length=1, choices=LETTER_CHOICES,null=True, blank=True)
    alias = models.CharField(max_length=20, null=True, blank=True)    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='class_teacher_of', limit_choices_to={'user_type': 'T'}, verbose_name="Class Teacher")
    total_students = models.PositiveIntegerField(default=0)
    class_monitor_boy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='monitor_boy_of', limit_choices_to={'user_type': 'STU'},)
    class_monitor_girl = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='monitor_girl_of', limit_choices_to={'user_type': 'STU'},)
    subjects = models.ManyToManyField(Subject, related_name='classes')    
    history = HistoricalRecords()
       
    def __str__(self):
        return f"{self.name} {self.section or ''}"
