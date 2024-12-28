from django import forms
from .models import Exams, ExamScore
from django.db import IntegrityError
from django.forms import ValidationError

class ExamsForm(forms.ModelForm):
    class Meta:
        model = Exams
        # fields = ['exam', 'class_name', 'start_date', 'end_date', 'result_date', 'note']
        fields = '__all__'
        exclude = ['academic_year', 'history']
        widgets = {
            'exam': forms.Select(attrs={'class': 'form-select'}, ),
            'class_name': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'result_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'note': forms.Textarea(attrs={'class': 'form-control'}),        
        }
        labels = {
            'exam': 'Exam',
            'class_name': 'Class',
            'exam_date': 'Exam Date',
            'exam_time': 'Exam Time',
            'exam_subject': 'Exam Subject',
            'exam_class': 'Exam Class',
            'exam_term': 'Exam Term',
        }        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply 'form-control' class to all fields
        self.fields['exam'].choices = [('', 'Select an Exam')] + list(self.fields['exam'].choices)[1:]
        self.fields['class_name'].choices = [('', 'Select a Class')] + list(self.fields['class_name'].choices)[1:]
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_classes} form-control".strip()
            # Add 'is-invalid' class if field has errors
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        result_date = cleaned_data.get('result_date')
        

        # Validation: End date not earlier than start date
        if start_date and end_date and end_date < start_date:
            self.add_error('end_date', "End Date cannot be earlier than Start Date.")

        # Validation: Result date not earlier than end date
        if end_date and result_date and result_date < end_date:
            self.add_error('result_date', "Result Date cannot be earlier than End Date.")
        return cleaned_data

    def save(self, *args, **kwargs):
            try:
                return super().save(*args, **kwargs)
            except IntegrityError:
                # Catch IntegrityError and add non-field error
                self.add_error(None, "This exam, class, and academic year combination already exists.")
                raise ValidationError("This exam, class, and academic year combination already exists.")