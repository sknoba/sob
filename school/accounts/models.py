from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import RegexValidator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from simple_history.models import HistoricalRecords
from core.utils import generate_random_number, INDIAN_STATES

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('M', 'Management Admin'),        
        ('STA', 'Staff'),
        ('P', 'Principal'),
        ('T', 'Teacher'),
        ('STU', 'Student'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    user_id = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):        
        if not self.is_superuser:
            if not self.user_id:
                self.generate_user_id()        
                while User.objects.filter(user_id=self.user_id).exists():
                    self.generate_user_id()
        super().save(*args, **kwargs)

    def generate_user_id(self):
        if self.user_type == 'M':
            self.user_id = f"MAG-{generate_random_number()}"
        elif self.user_type == 'STA':
            self.user_id = f"STAFF-{generate_random_number()}"
        elif self.user_type == 'P':
            self.user_id = f"PRN-{generate_random_number()}"
        elif self.user_type == 'T':
            self.user_id = f"TCH-{generate_random_number()}"
        elif self.user_type == 'STU':
            self.user_id = f"STU-{generate_random_number(length=5,alpha=True)}"      

    def __str__(self):
        if self.user_type != 'STU':            
            return self.get_full_name()
        elif self.user_type == 'STU':
            return self.student.get_full_name()   
        else:
            return self.username
        



class Profile(models.Model):
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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')    
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    photo = models.ImageField(upload_to='user_profile_photos/', blank=True, null=True, verbose_name="User Photo", help_text="Upload a valid image file (JPG, PNG, etc.) not exceeding 500 KB.")
    contact_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$')])    
    whatsapp_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$')])
    relation_status = models.CharField(max_length=1, choices=RELATION_STATUS_CHOICES)    
    adhar_number = models.CharField(max_length=12, validators=[RegexValidator(r'^\d{12}$')])
    bio = models.TextField(blank=True)

    # Address fields
    address_line_1 = models.CharField(max_length=255,)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=2, choices=INDIAN_STATES)        
    pin_code = models.CharField(max_length=6, validators=[RegexValidator(r'^\d{6}$')])
    
    # Education & Experience
    education = models.CharField(max_length=50)
    experience = models.CharField(max_length=50, help_text="As a Teacher or in any other field", null=True, blank=True)
    year_of_experience = models.CharField(max_length=12, default=0, verbose_name='Years of Experience')
    field_of_study = models.CharField(max_length=50, verbose_name='Field of Study', null=True, blank=True)
    certificate = models.CharField(max_length=50, verbose_name='Certificate', null=True, blank=True)
    achivements = models.CharField(max_length=50, verbose_name='Achivements', null=True, blank=True)
    
    # Employment & Specializations
    employment_type = models.CharField(max_length=2, choices=EMPLOYMENT_TYPE_CHOICES, verbose_name='Employment Type')    
    subjects = models.ManyToManyField('core.Subject', blank=True, verbose_name="Subject Taught")
    specializations = models.CharField(max_length=50,blank=True, verbose_name="Specializ In")
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile"
    
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):    
    if instance.user_type != 'STU':
        if created:
            Profile.objects.create(user=instance)
        else:
            profile, created = Profile.objects.get_or_create(user=instance)                
            profile.save()
    else:
        pass


class WebPushSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_info = models.JSONField()



    # def save(self, *args, **kwargs):
    #     if not self.student_id:
    #         # Generate the student_id if it's not set
    #         self.student_id = self.generate_student_id()

    #         # Ensure the generated student_id is unique
    #         while Student.objects.filter(student_id=self.student_id).exists():
    #             self.student_id = self.generate_student_id()

    #     super().save(*args, **kwargs)