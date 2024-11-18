from django import forms
from .models import Attendance
from .models import Student




class AttendanceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        students = kwargs.pop('students', None)
        super().__init__(*args, **kwargs)
        if students:
            for student in students:
                self.fields[f'attendance-{student.id}'] = forms.BooleanField(
                    required=False, label=student.get_full_name(), widget=forms.CheckboxInput()
                )