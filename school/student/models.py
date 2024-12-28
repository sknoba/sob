from django.db import models
from core.models import AcademicYear, Class
# from fees.models import FeesCollection
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
import uuid
from django.core.validators import RegexValidator
from core.utils import INDIAN_STATES
from accounts.models import User
from core.forms import current_academic_year

RELIGION_CHOICES = [
        ('christianity', 'Christianity'),
        ('islam', 'Islam'),
        ('hinduism', 'Hinduism'),
        ('buddhism', 'Buddhism'),
        ('judaism', 'Judaism'),
        ('sikhism', 'Sikhism'),
        ('atheism', 'Atheism'),
        ('other', 'Other'),
    ]

class Student(models.Model):
    # Student details
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student', null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    adhar_number = models.CharField(
        max_length=12,  # Ensures the field allows a maximum of 12 characters
        validators=[RegexValidator(r'^\d{12}$', message="Aadhar number must be exactly 12 digits.")],
        unique=True,  # Enforces uniqueness in the database
        verbose_name="Aadhar Number"
    )
    religion = models.CharField(max_length=50, choices=RELIGION_CHOICES)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True, verbose_name="Student Photo", help_text="Upload a valid image file (JPG, PNG, etc.) not exceeding 500 KB.", height_field=None, width_field=None)
    profile_creation_date = models.DateField(auto_now_add=True)
    
    # Previous School Details
    last_school_name = models.CharField(max_length=255)
    last_class_attended = models.CharField(max_length=100)
    examination_board = models.CharField(max_length=100)
    percentage_or_grade = models.CharField(max_length=50)  # Can store percentage or grade
    leaving_certificate_date = models.DateField(null=True, blank=True)
    leaving_certificate_number = models.CharField(max_length=100)

    # Address 
    nationality = models.CharField(max_length=10, choices=[('in', 'India'), ('o', 'Other')])

    residential_address = models.TextField(max_length=70)
    residential_city = models.CharField(max_length=100)
    residential_state = models.CharField(max_length=100 , choices=INDIAN_STATES)
    residential_pin_code = models.CharField(max_length=6, validators=[RegexValidator(r'^\d{6}$')])

    permanent_address = models.TextField(max_length=70)
    permanent_city = models.CharField(max_length=100)
    permanent_state = models.CharField(max_length=100, choices=INDIAN_STATES)
    permanent_pin_code = models.CharField(max_length=6, validators=[RegexValidator(r'^\d{6}$')])


    # Family Details
    # Guardian details (optional if neither parent is available)
    local_guardian_name = models.CharField(max_length=100, null=True, blank=True)
    local_guardian_mobile = models.CharField(max_length=15, null=True, blank=True)
    local_guardian_address = models.TextField(null=True, blank=True)
    local_guardian_health_problem = models.TextField(null=True, blank=True)
    relation_to_guardian = models.CharField(max_length=50, blank=True, null=True, help_text="Relation to the guardian, e.g. Uncle, Aunt")

    # Father Details
    father_name = models.CharField(max_length=100)
    father_age = models.IntegerField(null=True, blank=True)
    father_education = models.CharField(max_length=100, null=True, blank=True)
    father_occupation = models.CharField(max_length=100, null=True, blank=True)
    father_organisation = models.CharField(max_length=100, null=True, blank=True)
    father_designation = models.CharField(max_length=100,null=True, blank=True)
    father_languages_known = models.CharField(max_length=200, null=True, blank=True)
    father_mobile_number = models.CharField(max_length=10)
    father_email = models.EmailField(null=True, blank=True)
    father_phone = models.CharField(max_length=20, null=True, blank=True)
    father_annual_income = models.DecimalField(max_digits=12, decimal_places=2,null=True, blank=True)

    # Mother Details
    mother_name = models.CharField(max_length=100)
    mother_age = models.IntegerField(null=True, blank=True)
    mother_education = models.CharField(max_length=100,null=True, blank=True)
    mother_occupation = models.CharField(max_length=100,null=True, blank=True)
    mother_organisation = models.CharField(max_length=100,null=True, blank=True)
    mother_designation = models.CharField(max_length=100,null=True, blank=True)
    mother_languages_known = models.CharField(max_length=200, null=True, blank=True)
    mother_mobile_number = models.CharField(max_length=10)
    mother_email = models.EmailField(null=True, blank=True)
    mother_phone = models.CharField(max_length=20,null=True, blank=True)
    mother_annual_income = models.DecimalField(max_digits=12, decimal_places=2,null=True, blank=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='enrollments')
    standard = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    cancel_enroll = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student','academic_year')
    
    def save(self, *args, **kwargs):
        if self.id:
            self.academic_year = current_academic_year()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.student} - {self.standard} - {self.academic_year}'

#Update Total Student in Class Model After Enrollment
@receiver(post_save, sender=Enrollment)
def update_total_students_on_enrollment(sender, instance, created, **kwargs):
    if created:
        class_instance = instance.standard
        class_instance.total_students = class_instance.enrollments.count()
        class_instance.save()

@receiver(post_delete, sender=Enrollment)
def update_total_students_on_enrollment_delete(sender, instance, **kwargs):
    class_instance = instance.standard
    class_instance.total_students = class_instance.enrollments.count()
    class_instance.save()


# Create or Delete a user for the student when a new student is created
@receiver(post_save, sender=Enrollment)
def create_user_on_student_create(sender, instance, created, **kwargs):    
    if created and not instance.student.user:        
        student = instance.student
        first_name = student.first_name.lower() if hasattr(student, 'first_name') else ''
        last_name = student.last_name.lower() if hasattr(student, 'last_name') else ''
        aadhar_number = student.adhar_number if hasattr(student, 'adhar_number') else ''
        
        # Generate username
        username_prefix = (first_name[:4] if len(first_name) >= 4 else first_name + last_name[:4 - len(first_name)])
        username_suffix = aadhar_number[-4:] if len(aadhar_number) >= 4 else ''
        username = f"{username_prefix}{username_suffix}"
        
        # Generate password
        date_of_birth = student.date_of_birth.strftime('%d%m%y') if hasattr(student, 'date_of_birth') and student.date_of_birth else '000000'
        password = f"{username_prefix.capitalize()}@{date_of_birth}"       
        # Create the user
        user = User.objects.create_user(username=username, password=password, user_type='STU')
        student.user = user
        student.save()

 
@receiver(post_delete, sender=Student)
def delete_user_on_student_delete(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()