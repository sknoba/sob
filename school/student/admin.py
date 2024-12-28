from django.contrib import admin
from .models import Enrollment, Student
from django.utils.html import format_html

 
from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

    # Optionally, you can use widgets or fields to group father/mother fields into columns
    # For now, it's more about layout control in `fieldsets` and admin customization

class StudentAdmin(admin.ModelAdmin):
    form = StudentForm
    # List view configuration
    list_display = ('get_full_name', 'gender', 'religion', 'date_of_birth', 'nationality', 'last_school_name', 'father_name', 'mother_name', 'photo_preview')
    list_filter = ('gender', 'religion', 'nationality')
    search_fields = ['first_name', 'last_name', 'adhar_number']
    # Form view configuration
    readonly_fields = ('profile_creation_date',)
    fieldsets = (
        ('Student Details', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'gender', 'adhar_number', 'religion', 'photo', 'profile_creation_date')
        }),
        ('Previous School Details', {
            'fields': ('last_school_name', 'last_class_attended', 'examination_board', 'percentage_or_grade', 'leaving_certificate_date', 'leaving_certificate_number')
        }),
        ('Address Information', {
            'fields': ('nationality', 'residential_address', 'residential_city', 'residential_state', 'residential_pin_code', 'permanent_address', 'permanent_city', 'permanent_state', 'permanent_pin_code')
        }),
        ('Family Details', {
            'fields': (
                ('father_name', 'mother_name'),
                ('father_age', 'mother_age'),
                ('father_education', 'mother_education'),
                ('father_occupation', 'mother_occupation'),
                ('father_organisation', 'mother_organisation'),
                ('father_designation', 'mother_designation'),
                ('father_languages_known', 'mother_languages_known'),
                ('father_mobile_number', 'mother_mobile_number'),
                ('father_email', 'mother_email'),
                ('father_phone', 'mother_phone'),
                ('father_annual_income', 'mother_annual_income')
            )
        }),
        ('Guardian Details (if applicable)', {
            'fields': ('local_guardian_name', 'local_guardian_mobile', 'local_guardian_address', 'local_guardian_health_problem', 'relation_to_guardian')
        }),
    )

    # Exclude the 'profile_creation_date' from the form fields
    exclude = ('profile_creation_date',)

    # Add image preview for photo field in list view
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="100" height="100"/>'.format(obj.photo.url))
        return "No Image"
    photo_preview.short_description = 'Photo Preview'

    # Optional: Add custom actions (e.g., Mark as graduated)
    actions = ['mark_as_graduated']

    def mark_as_graduated(self, request, queryset):
        queryset.update(last_class_attended='Graduated')
        self.message_user(request, "Marked selected students as graduated")
    mark_as_graduated.short_description = "Mark selected students as graduated"

admin.site.register(Student, StudentAdmin)



@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'academic_year', 'standard', 'enrollment_date', 'id')
    list_filter = ('academic_year', 'standard')
    search_fields = ('student__first_name', 'student__last_name', 'student__student_id')
    ordering = ('-enrollment_date',)

    def get_inline_instances(self, request, obj=None):
        inline_instances = super().get_inline_instances(request, obj)
        for inline in inline_instances:
            # Set the parent object for filtering
            inline.parent_object = obj
        return inline_instances

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
    
        # Example: Make 'academic_year' read-only when obj is not None (i.e., when it's being edited, not created)
        if obj:  # obj is None when creating a new object
            readonly_fields += ('academic_year', 'student', 'standard' )
        
        return readonly_fields