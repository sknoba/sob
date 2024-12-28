from django import forms
from .models import Subject, AcademicYear, Class
from django.contrib.auth.forms import UserChangeForm
from accounts.models import User
from django.utils import timezone

def current_academic_year():
    return AcademicYear.objects.get(start_date__lte=timezone.now().date(), end_date__gte=timezone.now().date())

class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        fields = ['start_date', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),            
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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


def get_boy_list(class_id):
    from student.models import Enrollment
    return Enrollment.objects.all().filter(academic_year=current_academic_year()).filter(standard=class_id)

class ClassCreateForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'alias','section']
        # Adding widgets for better form control and styling
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter standard name', }),
            'alias': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter standard alias'}),
            'section': forms.Select(attrs={'class': 'form-control',}),            

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

class ClassUpdateFrom(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'alias','section', 'user', 'class_monitor_boy', 'class_monitor_girl']
        # Adding widgets for better form control and styling
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter standard name', }),
            'alias': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter standard alias'}),
            'section': forms.Select(attrs={'class': 'form-control',}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'class_monitor_boy': forms.Select(attrs={'class': 'form-control'}),
            'class_monitor_girl': forms.Select(attrs={'class': 'form-control'}),
        }
    

        
        # class_monitor_boy = forms.ModelChoiceField(
        # queryset=get_boy_list(self.object),  # Adjust according to your model
        # required=False,
        # widget=forms.Select(attrs={'class': 'form-control'})
        # )
        # class_monitor_girl = forms.ModelChoiceField(
        # queryset=Class.objects.all(),  # Adjust according to your model
        # required=False,
        # widget=forms.Select(attrs={'class': 'form-control'})
        # )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply 'form-control' class to all fields
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_classes} form-control".strip()
            # Add 'is-invalid' class if field has errors
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter subject name', }),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter subject code'}),            
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