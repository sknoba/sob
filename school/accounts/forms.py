from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import User, Profile
from django.core.exceptions import ValidationError
import re



class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

        # Adding widgets for better form control and styling
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name', 'id': 'firstName'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name', 'id': 'lastName'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'id': 'username', 'disabled': 'disabled'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'id': 'email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'password'}),            
        }
    # Custom validation for first name (only letters)
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise ValidationError("First name should only contain letters.")
        return first_name
    
        # Custom validation for last name (only letters)
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise ValidationError("Last name should only contain letters.")
        return last_name

    def clean_password(self):
        password = self.cleaned_data.get('password')

        # Check password length
        if len(password) < 8:
            raise ValidationError("Your password must contain at least 8 characters.")

        # Check if password contains only numbers (entirely numeric)
        if password.isdigit():
            raise ValidationError("Your password can't be entirely numeric.")

        # Check if password is too similar to other personal information
        # (For simplicity, just check if the password contains the username or email part)
        username = self.cleaned_data.get('username', '')
        email = self.cleaned_data.get('email', '')

        if username and username.lower() in password.lower():
            raise ValidationError("Your password can’t be too similar to your username.")
        if email and email.split('@')[0].lower() in password.lower():
            raise ValidationError("Your password can’t be too similar to your email.")

        # Check if the password is a commonly used password (can be expanded with more examples)
        common_passwords = ['123456', 'password', 'qwerty', '12345', 'letmein']
        if password.lower() in common_passwords:
            raise ValidationError("Your password can’t be a commonly used password.")

        return password

    # Custom validation for username (allow letters, numbers, underscores, and periods)
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Regex to match letters, numbers, underscores, and periods
        if not re.match(r'^[a-zA-Z0-9_.]+$', username):
            raise ValidationError("Username can only contain letters, numbers, underscores, and periods.")
        return username




    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply 'form-control' class to all fields
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_classes} form-control".strip()
            # Add 'is-invalid' class if field has errors
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'


    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')    
    # date_of_birth = models.DateField(null=True, blank=True)
    # gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    # photo = models.ImageField(upload_to='user_profile_photos/', blank=True, null=True, verbose_name="User Photo", help_text="Upload a valid image file (JPG, PNG, etc.) not exceeding 500 KB.")
    # contact_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$')])    
    # whatsapp_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$')])
    # relation_status = models.CharField(max_length=1, choices=RELATION_STATUS_CHOICES)    
    # adhar_number = models.CharField(max_length=12, validators=[RegexValidator(r'^\d{12}$')])
    # bio = models.TextField(blank=True)

    # # Address fields
    # address_line_1 = models.CharField(max_length=255,)
    # address_line_2 = models.CharField(max_length=255, blank=True)
    # city = models.CharField(max_length=100)
    # district = models.CharField(max_length=100)
    # state = models.CharField(max_length=2, choices=INDIAN_STATES)        
    # pin_code = models.CharField(max_length=6, validators=[RegexValidator(r'^\d{6}$')])
    
    # # Education & Experience
    # education = models.CharField(max_length=50)
    # experience = models.CharField(max_length=50, help_text="As a Teacher or in any other field")
    # year_of_experience = models.CharField(max_length=12, default=0, verbose_name='Years of Experience')
    # field_of_study = models.CharField(max_length=50, verbose_name='Field of Study')
    # certificate = models.CharField(max_length=50, verbose_name='Certificate', null=True, blank=True)
    # achivements = models.CharField(max_length=50, verbose_name='Achivements', null=True, blank=True)
    
    # # Employment & Specializations
    # employment_type = models.CharField(max_length=2, choices=EMPLOYMENT_TYPE_CHOICES, verbose_name='Employment Type')    
    # subjects = models.ManyToManyField('core.Subject', blank=True, verbose_name="Subject Taught")
    # specializations = models.CharField(max_length=50,blank=True, verbose_name="Specializ In")
    # history = HistoricalRecords()

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth','gender','photo','contact_number','whatsapp_number','relation_status','adhar_number','bio','address_line_1','address_line_2','city','district','state','pin_code','education','experience','year_of_experience','field_of_study','certificate','achivements','employment_type','subjects','specializations']

        # Adding widgets for better form control and styling
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),            
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'id': 'id_photo', 'style':'display: none;', 'onchange':'previewImage(event)'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control'}),
            'relation_status': forms.Select(attrs={'class': 'form-control'}),
            'adhar_number': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'pin_code': forms.TextInput(attrs={'class': 'form-control'}),            
            'education': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.TextInput(attrs={'class': 'form-control'}),
            'year_of_experience': forms.TextInput(attrs={'class': 'form-control'}),
            'field_of_study': forms.TextInput(attrs={'class': 'form-control'}),
            'certificate': forms.TextInput(attrs={'class': 'form-control'}),
            'achivements': forms.TextInput(attrs={'class': 'form-control'}),            
            'employment_type': forms.Select(attrs={'class': 'form-control'}),
            'subjects': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'subjects'}),
            'specializations': forms.TextInput(attrs={'class': 'form-control'}),            
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply 'form-control' class to all fields
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_classes} form-control".strip()
            # Add 'is-invalid' class if field has errors
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'




class UserCreateAccessForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']  

    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply 'form-control' class to all fields
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_classes} form-control".strip()
            # Add 'is-invalid' class if field has errors
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'

class UserAccessUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'is_active', 'first_name', 'last_name', 'email', 'groups', 'user_permissions']

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply 'form-control' class to all fields
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_classes} form-control".strip()
            # Add 'is-invalid' class if field has errors
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'






# class UserCreateAccessForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email']  

#     first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     last_name = forms.CharField(required=True)
#     email = forms.EmailField(required=True)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Apply 'form-control' class to all fields
#         for field_name, field in self.fields.items():
#             existing_classes = field.widget.attrs.get('class', '')
#             field.widget.attrs['class'] = f"{existing_classes} form-control".strip()
#             # Add 'is-invalid' class if field has errors
#             if self.errors.get(field_name):
#                 field.widget.attrs['class'] += ' is-invalid'

# class UserAccessUpdateForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ['username', 'is_active', 'first_name', 'last_name', 'email', 'groups', 'user_permissions']

#     first_name = forms.CharField(required=True)
#     last_name = forms.CharField(required=True)
#     email = forms.EmailField(required=True)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Apply 'form-control' class to all fields
#         for field_name, field in self.fields.items():
#             existing_classes = field.widget.attrs.get('class', '')
#             field.widget.attrs['class'] = f"{existing_classes} form-control".strip()
#             # Add 'is-invalid' class if field has errors
#             if self.errors.get(field_name):
#                 field.widget.attrs['class'] += ' is-invalid'


# # class UserProfileForm(forms.ModelForm):
# #     class Meta:
# #         model = User
# #         fields = ['acc_type','date_of_birth', 'gender', 'acc_id', 'photo', 'phone_number', 'relation_status', 'address_line_1', 'address_line_2', 'city', 'district', 'state', 'pin_code', 'education', 'subjects', 'employment_type']

# #         # Adding widgets for better form control and styling
# #         widgets = {
# #             'acc_type' : forms.Select(attrs={'class': 'form-control'}),
# #             'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
# #             'gender': forms.Select(attrs={'class': 'form-control'}),
# #             'acc_id': forms.TextInput(attrs={'class': 'form-control disabled', 'readonly': 'readonly'}),
# #             'photo': forms.FileInput(attrs={'class': 'form-control'}),
# #             'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
# #             'relation_status': forms.Select(attrs={'class': 'form-control'}),
# #             'address_line_1': forms.TextInput(attrs={'class': 'form-control'}),
# #             'address_line_2': forms.TextInput(attrs={'class': 'form-control'}),
# #             'city': forms.TextInput(attrs={'class': 'form-control'}),
# #             'district': forms.TextInput(attrs={'class': 'form-control'}),
# #             'state': forms.Select(attrs={'class': 'form-control'}),
# #             'pin_code': forms.TextInput(attrs={'class': 'form-control'}),
# #             'education': forms.TextInput(attrs={'class': 'form-control'}),
# #             'subjects': forms.SelectMultiple(attrs={'class': 'form-control'}),
# #             'employment_type': forms.Select(attrs={'class': 'form-control'}),
# #         }
# #     def __init__(self, *args, **kwargs):
# #         super().__init__(*args, **kwargs)
# #         # Apply 'form-control' class to all fields
# #         for field_name, field in self.fields.items():
# #             existing_classes = field.widget.attrs.get('class', '')
# #             field.widget.attrs['class'] = f"{existing_classes} form-control".strip()
# #             # Add 'is-invalid' class if field has errors
# #             if self.errors.get(field_name):
# #                 field.widget.attrs['class'] += ' is-invalid'