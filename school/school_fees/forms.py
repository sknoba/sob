from django import forms
from .models import FeesStructure, TransportFees, Invoince
from core.forms import current_academic_year

class FeesStructureForm(forms.ModelForm):
    class Meta:
        model = FeesStructure
        fields = ['class_name', 'school_fee']

        widgets = {
            'class_name': forms.Select(attrs={'class': 'form-control'}),
            'school_fee': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        # Check for existing FeesStructure with the same class_name and academic_year
        class_name = cleaned_data.get('class_name')
        academic_year = current_academic_year()

        if class_name and academic_year:
            # Check if a FeesStructure with this class_name and academic_year already exists
            if FeesStructure.objects.filter(class_name=class_name, academic_year=academic_year).exists():
                raise forms.ValidationError(
                    f"A fees structure already exists of {class_name} for {academic_year}.",
                    code='unique_constraint'
                )
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply 'form-control' class to all fields
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_classes} form-control".strip()
            # Add 'is-invalid' class if field has errors
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'
    

class TranportFeesForm(forms.ModelForm):
    class Meta:
        model = TransportFees
        fields = ['bus_route', 'transport_fee']

        widgets = {
            'bus_route': forms.TextInput(attrs={'class': 'form-control'}),
            'transport_fee': forms.NumberInput(attrs={'class': 'form-control'}),
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



class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoince
        fields = ['school_fee', 'transport_fee', 'payment_method', 'remarks']
        widgets = {
            'school_fee': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}),
            'transport_fee' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Remarks - Admition fees, Installment etc...'}),
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














# class FeesCollectionForm(forms.ModelForm):
#     class Meta:
#         model = FeesCollection
#         fields = ['total_fees', 'due_date']
#         widgets = {
#             'total_fees': forms.NumberInput(attrs={'class': 'form-control'}),
#             'due_date': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Apply 'form-control' class to all fields
#         for field_name, field in self.fields.items():
#             existing_classes = field.widget.attrs.get('class', '')
#             field.widget.attrs['class'] = f"{existing_classes} form-control".strip()
#             # Add 'is-invalid' class if field has errors
#             if self.errors.get(field_name):
#                 field.widget.attrs['class'] += ' is-invalid'