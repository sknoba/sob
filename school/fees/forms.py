from django import forms
from .models import Invoice , FeesCollection


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['amount_paid', 'payment_method', 'remarks']
        widgets = {
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}),
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

class FeesCollectionForm(forms.ModelForm):
    class Meta:
        model = FeesCollection
        fields = ['total_fees', 'due_date']
        widgets = {
            'total_fees': forms.NumberInput(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
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