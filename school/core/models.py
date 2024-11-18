from django.db import models, transaction
from django.db.models import Max
import uuid
from django.core.validators import RegexValidator
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Generate a unique Student ID
def generate_id():
    return str(uuid.uuid4())[:8].upper()

def generate_sub_code():
    return str(uuid.uuid4())[:5].upper()

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

DISTRICTS_MAHARASHTRA = [
    ('AHMADNAGAR', 'Ahmadnagar'),
    ('AKOLA', 'Akola'),
    ('AMRAVATI', 'Amravati'),
    ('AURANGABAD', 'Aurangabad'),
    ('BULDHANA', 'Buldhana'),
    ('CHANDRAPUR', 'Chandrapur'),
    ('DHULE', 'Dhule'),
    ('GADCHIROLI', 'Gadchiroli'),
    ('GONDIA', 'Gondia'),
    ('HINGOLI', 'Hingoli'),
    ('JALNA', 'Jalna'),
    ('JALGAON', 'Jalgaon'),
    ('LATUR', 'Latur'),
    ('NAGPUR', 'Nagpur'),
    ('NANDURBAR', 'Nandurbar'),
    ('NASHIK', 'Nashik'),
    ('OSMANABAD', 'Osmanabad'),
    ('PARBHANI', 'Parbhani'),
    ('PUNE', 'Pune'),
    ('RAIGAD', 'Raigad'),
    ('RATNAGIRI', 'Ratnagiri'),
    ('SANGLI', 'Sangli'),
    ('SATARA', 'Satara'),
    ('SOLAPUR', 'Solapur'),
    ('THANE', 'Thane'),
    ('WASHIM', 'Washim'),
    ('YAVATMAL', 'Yavatmal'),
]
TALUKAS_YAVATMAL = [
    ('YAVATMAL', 'Yavatmal'),
    ('PUSAD', 'Pusad'),
    ('DIGRAS', 'Digras'),
    ('WADSA', 'Wadsa'),
    ('MAHAGAON', 'Mahagaon'),
    ('KELAPUR', 'Kelapur'),
    ('RALEGAON', 'Ralegaon'),
    ('VANI', 'Vani'),
    ('ARNI', 'Arni'),
    ('CHANDAI', 'Chandai'),
]


# Example usage in a Django model
from django.db import models

class AcademicYear(models.Model):
    name = models.CharField(
        max_length=20,
        help_text='The name must be in the format YYYY-YY (e.g., 2024-25)',
        validators=[RegexValidator(
            regex=r'^\d{4}-\d{2}$',
            message='The name must be in the format YYYY-YY (e.g., 2024-25)',            
        )]
    )
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Student(models.Model):
    # Student details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    student_id = models.CharField(max_length=8, unique=True, default=generate_id, null=True)
    create_date = models.DateField(auto_now_add=True)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    # Address fields
    address_line_1 = models.CharField(max_length=255, null=True, blank=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100,)
    state = models.CharField(max_length=50, choices=INDIAN_STATES)
    pin_code = models.CharField(max_length=6, validators=[RegexValidator(r'^\d{6}$')])

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


    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.student_id}"


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    RELATION_STATUS_CHOICES = (
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    )
    EMPLOYMENT_TYPE_CHOICES = (
        ('PE', 'Permanent Employee'),
        ('CE', 'Contract Employee'),
    )
    ACCOUNT_TYPE_CHOICES = (
        ('TS', 'Taching Staff'),
        ('NT', 'Non Teaching Staff'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    acc_type = models.CharField(max_length=2, choices=ACCOUNT_TYPE_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    acc_id = models.CharField(max_length=20, unique=True, default=generate_id, null=True)
    photo = models.ImageField(upload_to='user_profile_photos/')
    phone_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$')])
    relation_status = models.CharField(max_length=1, choices=RELATION_STATUS_CHOICES)
    
    # Address fields
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=50, choices=INDIAN_STATES)
    pin_code = models.CharField(max_length=6, validators=[RegexValidator(r'^\d{6}$')])
    
    # Extra fields
    education = models.CharField(max_length=50)
    subjects = models.ManyToManyField('Subject', related_name='subject_teaching', blank=True)
    employment_type = models.CharField(max_length=2, choices=EMPLOYMENT_TYPE_CHOICES)


    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
        instance.userprofile.save()
    

LETTER_CHOICES = [(chr(i), chr(i)) for i in range(ord('A'), ord('Z') + 1)]

class Standard(models.Model):
    name = models.CharField(max_length=50)
    section = models.CharField(max_length=1, choices=LETTER_CHOICES,null=True, blank=True)
    alias = models.CharField(max_length=20, null=True, blank=True)    
    class_teacher = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True,related_name='class_teacher_of')
    class_monitor_boy = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, related_name='monitor_boy_of')
    class_monitor_girl = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, related_name='monitor_girl_of')

    def __str__(self):
        return f"{self.name} {self.section or ''}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True, default=generate_sub_code)

    def __str__(self):
        return self.name