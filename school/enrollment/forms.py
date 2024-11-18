from django import forms
from .models import Enrollment

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['academic_year', 'standard']
        widgets = {
            'academic_year': forms.Select(attrs={'class': 'form-control'}),
            'standard': forms.Select(attrs={'class': 'form-control'}),
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