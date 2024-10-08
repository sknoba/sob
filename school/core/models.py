from django.db import models
import uuid
from django.core.validators import RegexValidator
from django.utils.crypto import get_random_string

# Generate a unique Student ID
def generate_id():
    return str(uuid.uuid4())[:8].upper()


INDIAN_STATES = [
    ('AP', 'Andhra Pradesh'),
    ('AR', 'Arunachal Pradesh'),
    ('AS', 'Assam'),
    ('BR', 'Bihar'),
    ('CT', 'Chhattisgarh'),
    ('GA', 'Goa'),
    ('GJ', 'Gujarat'),
    ('HR', 'Haryana'),
    ('HP', 'Himachal Pradesh'),
    ('JH', 'Jharkhand'),
    ('KA', 'Karnataka'),
    ('KL', 'Kerala'),
    ('MP', 'Madhya Pradesh'),
    ('MH', 'Maharashtra'),
    ('MN', 'Manipur'),
    ('ML', 'Meghalaya'),
    ('MZ', 'Mizoram'),
    ('NL', 'Nagaland'),
    ('OR', 'Odisha'),
    ('PB', 'Punjab'),
    ('RJ', 'Rajasthan'),
    ('SK', 'Sikkim'),
    ('TN', 'Tamil Nadu'),
    ('TG', 'Telangana'),
    ('TR', 'Tripura'),
    ('UP', 'Uttar Pradesh'),
    ('UT', 'Uttarakhand'),
    ('WB', 'West Bengal'),
    ('AN', 'Andaman and Nicobar Islands'),
    ('CH', 'Chandigarh'),
    ('DN', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('LD', 'Lakshadweep'),
    ('DL', 'Delhi'),
    ('JK', 'Jammu and Kashmir'),
    ('LA', 'Ladakh'),
    ('PY', 'Puducherry')
]

class Student(models.Model):
    # Student details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    student_id = models.CharField(max_length=8, unique=True, default=generate_id)
    enrollment_date = models.DateField(auto_now_add=True)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    standard = models.ForeignKey('Standard', on_delete=models.SET_NULL, null=True, blank=True)

    # Address fields
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=50, choices=INDIAN_STATES)
    pin_code = models.CharField(max_length=20, validators=[RegexValidator(r'^\d{6}$')])

    # Father's details
    father_name = models.CharField(max_length=100)
    father_phone = models.CharField(max_length=15, blank=True, null=True)
    father_email = models.EmailField(blank=True, null=True)

    # Mother's details
    mother_name = models.CharField(max_length=100)
    mother_phone = models.CharField(max_length=15, blank=True, null=True)
    mother_email = models.EmailField(blank=True, null=True)

    # Guardian details (optional if neither parent is available)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_phone = models.CharField(max_length=15, blank=True, null=True)
    guardian_email = models.EmailField(blank=True, null=True)
    relation_to_guardian = models.CharField(max_length=50, blank=True, null=True, help_text="Relation to the guardian, e.g. Uncle, Aunt")

    def save(self, *args, **kwargs):
        if not self.student_id:
            # Generate a unique student_id
            base_id = f"{self.first_name[:3].upper()}{self.last_name[:3].upper()}"
            random_suffix = get_random_string(5, '0123456789')
            self.student_id = f"{base_id}{random_suffix}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.student_id}"


class Teacher(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    RELATION_STATUS_CHOICES = (
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    )
    EMPLOYMENT_TYPE_CHOICES = (
        ('FT', 'Full Time'),
        ('PT', 'Part Time'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    teacher_id = models.CharField(max_length=20, unique=True, default=generate_id)
    joining_date = models.DateField()
    photo = models.ImageField(upload_to='teacher_photos/', null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    relation_status = models.CharField(max_length=1, choices=RELATION_STATUS_CHOICES)
    
    # Address fields
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=6, validators=[RegexValidator(r'^\d{6}$')])
    
    # Extra fields
    education = models.TextField()
    subjects = models.ManyToManyField('Subject')
    employment_type = models.CharField(max_length=2, choices=EMPLOYMENT_TYPE_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.teacher_id})"
    


class Standard(models.Model):
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=20)
    class_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='class_teacher_of')
    class_monitor_boy = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, related_name='monitor_boy_of')
    class_monitor_girl = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, related_name='monitor_girl_of')

    def __str__(self):
        return f"{self.name} ({self.alias})"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name