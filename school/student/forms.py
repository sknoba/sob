from django import forms
from .models import Student, Enrollment 
from datetime import date
from django.core.exceptions import ValidationError
import re
from core.forms import current_academic_year
from core.models import AcademicYear
from school_fees.models import FeesCollection, FeesStructure






# Form for the first half of the model
class StudentFormStep1(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender', 'adhar_number', 'religion', 'photo',
            'last_school_name', 'last_class_attended', 'examination_board', 'percentage_or_grade', 
            'leaving_certificate_date', 'leaving_certificate_number',
        ]
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control', 'id': 'id_photo', 'style':'display: none;', 'onchange':'previewImage(event)'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'leaving_certificate_date': forms.DateInput(attrs={'type': 'date'}),
        }

    # Validator for first_name
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[a-zA-Z]+$', first_name):  # Regex for alphabetic characters only
            raise ValidationError("First name should contain only alphabetic characters.")
        return first_name

    # Validator for last_name
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[a-zA-Z]+$', last_name):  # Regex for alphabetic characters only
            raise ValidationError("Last name should contain only alphabetic characters.")
        return last_name

    # Validator for date_of_birth
    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob and dob > date.today():  # Checks if date_of_birth is in the future
            raise ValidationError("Date of birth cannot be a future date.")
        return dob

    # Validator for leaving_certificate_date
    def clean_leaving_certificate_date(self):
        leaving_date = self.cleaned_data.get('leaving_certificate_date')
        if leaving_date and leaving_date > date.today():  # Checks if leaving_certificate_date is in the future
            raise ValidationError("Leaving Certificate Date cannot be a future date.")
        return leaving_date

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            max_size_kb = 500  # Maximum file size in KB
            if photo.size > max_size_kb * 1024:  # Convert KB to bytes
                raise ValidationError(f"Photo size should not exceed {max_size_kb} KB.")
        return photo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply 'form-control' class to all fields
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_classes} form-control".strip()
            # Add 'is-invalid' class if field has errors
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'

# Form for the second half of the model
class StudentFormStep2(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'nationality', 'residential_address', 'residential_city', 'residential_state', 'residential_pin_code',
            'permanent_address', 'permanent_city', 'permanent_state', 'permanent_pin_code', 'local_guardian_name', 
            'local_guardian_mobile', 'local_guardian_address', 'local_guardian_health_problem', 'relation_to_guardian',
            'father_name', 'father_age', 'father_education', 'father_occupation', 'father_organisation', 'father_designation',
            'father_languages_known', 'father_mobile_number', 'father_email', 'father_phone', 'father_annual_income',
            'mother_name', 'mother_age', 'mother_education', 'mother_occupation', 'mother_organisation', 'mother_designation',
            'mother_languages_known', 'mother_mobile_number', 'mother_email', 'mother_phone', 'mother_annual_income',
        ]
        widgets = {
            'father_annual_income': forms.NumberInput(attrs={'step': '0.01'}),
            'mother_annual_income': forms.NumberInput(attrs={'step': '0.01'}),
            'residential_address': forms.Textarea(attrs={'rows': 3}),
            'permanent_address': forms.Textarea(attrs={'rows': 3}),
            'local_guardian_address': forms.Textarea(attrs={'rows': 3}),
            'local_guardian_health_problem': forms.Textarea(attrs={'rows': 3}),
        }


        # Validator for first_name
    def clean_father_name(self):
        father_name = self.cleaned_data.get('father_name')
        if not re.match(r'^[a-zA-Z]+$', father_name):  # Regex for alphabetic characters only
            raise ValidationError("First name should contain only alphabetic characters.")
        return father_name
    
    def clean_mother_name(self):
        mother_name = self.cleaned_data.get('mother_name')
        if not re.match(r'^[a-zA-Z]+$', mother_name):
            raise ValidationError("First name should contain only alphabetic characters.")
        return mother_name
    
    def clean_father_mobile_number(self):
        father_mobile_number = self.cleaned_data.get('father_mobile_number')
        if not re.match(r'^[6-9]\d{9}$', father_mobile_number):
            raise ValidationError("Enter a valid mobile number.")
        return father_mobile_number
    
    def clean_mother_mobile_number(self):
        mother_mobile_number = self.cleaned_data.get('mother_mobile_number')
        if not re.match(r'^[6-9]\d{9}$', mother_mobile_number):
            raise ValidationError("Enter a valid mobile number.")
        return mother_mobile_number



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply 'form-control' class to all fields
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_classes} form-control".strip()
            # Add 'is-invalid' class if field has errors
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['standard']
        widgets = {
            # 'academic_year': forms.Select(attrs={'class': 'form-control'}),
            'standard': forms.Select(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_classes} form-control".strip()
            # Add 'is-invalid' class if field has errors
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'

    def clean(self):
        # Check if there is an active academic year
        try:
            # Get the current academic year
            current_year = current_academic_year()
            if not current_year.is_active:
                raise ValidationError("The current academic year is not active.")
        except AcademicYear.DoesNotExist:
            raise ValidationError("There is no active academic year available.")

        # If the current academic year exists and is active, the form is valid
        return super().clean()



class FeesCollectionForm(forms.ModelForm):
    class Meta:
        model = FeesCollection
        fields = [
            'transport',                         
            'school_fee_concession', 
            'transport_fee_concession',             
        ]
        widgets = {            
            'transport': forms.Select(attrs={'class': 'form-control'}),
            'school_fee_concession': forms.NumberInput(attrs={'class': 'form-control'}),
            'transport_fee_concession': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    def clean(self):
        return super().clean()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_classes} form-control".strip()
            # Add 'is-invalid' class if field has errors
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'





class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender', 'adhar_number', 'religion', 'photo', 'last_school_name', 'last_class_attended', 'examination_board', 'percentage_or_grade', 'leaving_certificate_date', 'leaving_certificate_number',
            'nationality', 'residential_address', 'residential_city', 'residential_state', 'residential_pin_code',
            'permanent_address', 'permanent_city', 'permanent_state', 'permanent_pin_code', 'local_guardian_name',
            'local_guardian_mobile', 'local_guardian_address', 'local_guardian_health_problem', 'relation_to_guardian',
            'father_name', 'father_age', 'father_education', 'father_occupation', 'father_organisation', 'father_designation',
            'father_languages_known', 'father_mobile_number', 'father_email', 'father_phone', 'father_annual_income',
            'mother_name', 'mother_age', 'mother_education', 'mother_occupation', 'mother_organisation', 'mother_designation',
            'mother_languages_known', 'mother_mobile_number', 'mother_email', 'mother_phone', 'mother_annual_income',
        ]

        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control', 'id': 'id_photo', 'style':'display: none;', 'onchange':'previewImage(event)'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'leaving_certificate_date': forms.DateInput(attrs={'type': 'date'}),
            'father_annual_income': forms.NumberInput(attrs={'step': '0.01'}),
            'mother_annual_income': forms.NumberInput(attrs={'step': '0.01'}),
            'residential_address': forms.Textarea(attrs={'rows': 3}),
            'permanent_address': forms.Textarea(attrs={'rows': 3}),
            'local_guardian_address': forms.Textarea(attrs={'rows': 3}),
            'local_guardian_health_problem': forms.Textarea(attrs={'rows': 3}),
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