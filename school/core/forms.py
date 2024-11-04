from django import forms
from .models import Student, Teacher, Standard, Subject

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'photo', 'standard','student_id', 'address_line_1', 
                  'address_line_2', 'city','district', 'state', 'pin_code', 'father_name', 
                  'father_phone', 'father_email', 'mother_name', 'mother_phone', 'mother_email', 
                  'guardian_name', 'guardian_phone', 'guardian_email', 'relation_to_guardian']

        # Adding widgets for better form control and styling
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'id': 'id_photo', 'style':'display: none;', 'onchange':'previewImage(event)'}),
            'standard': forms.Select(attrs={'class': 'form-control'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control desable', 'readonly': 'readonly'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'pin_code': forms.TextInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'father_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'relation_to_guardian': forms.TextInput(attrs={'class': 'form-control'}),
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

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'teacher_id', 'joining_date', 'photo', 'phone_number', 'email', 'relation_status', 'address_line_1', 'address_line_2', 'city', 'district', 'state', 'pin_code', 'education', 'subjects', 'employment_type']

        # Adding widgets for better form control and styling
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'teacher_id': forms.TextInput(attrs={'class': 'form-control'}),
            'joining_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'relation_status': forms.Select(attrs={'class': 'form-control'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'pin_code': forms.TextInput(attrs={'class': 'form-control'}),
            'education': forms.Textarea(attrs={'class': 'form-control'}),
            'subjects': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'employment_type': forms.Select(attrs={'class': 'form-control'}),
        }

class StandardForm(forms.ModelForm):
    class Meta:
        model = Standard
        fields = ['name', 'alias','section', 'class_teacher', 'class_monitor_boy', 'class_monitor_girl']
        # Adding widgets for better form control and styling
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',}),
            'alias': forms.TextInput(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'class_teacher': forms.Select(attrs={'class': 'form-control'}),
            'class_monitor_boy': forms.Select(attrs={'class': 'form-control'}),
            'class_monitor_girl': forms.Select(attrs={'class': 'form-control'}),
        }

        class_teacher = forms.ModelChoiceField(
        queryset=Teacher.objects.all(),  # Adjust according to your model
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
        )
        class_monitor_boy = forms.ModelChoiceField(
        queryset=Student.objects.all(),  # Adjust according to your model
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
        )
        class_monitor_girl = forms.ModelChoiceField(
        queryset=Student.objects.all(),  # Adjust according to your model
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
        )
