from django.contrib import admin
from .models import Student, Standard, Teacher, Subject


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'full_name', 'gender', 'date_of_birth', 'enrollment_date', 'current_standard')
    list_filter = ('gender', 'enrollment_date', 'standard')
    search_fields = ('student_id', 'first_name', 'last_name', 'father_name', 'mother_name')
    readonly_fields = ('enrollment_date','student_id')
    exclude = ('student_id',)

    
    fieldsets = (
        ('Personal Information', {
            'fields': (('first_name', 'last_name'), 'date_of_birth', 'gender', 'photo')
        }),
        ('Academic Information', {
            'fields': ('student_id','standard')
        }),
        ('Contact Information', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'district', 'state', 'pin_code')
        }),
        ('Parent/Guardian Information', {   
            'fields': (('father_name', 'father_phone', 'father_email'),
                       ('mother_name', 'mother_phone', 'mother_email'),
                       ('guardian_name', 'guardian_phone', 'guardian_email', 'relation_to_guardian'))
        }),
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'

    def current_standard(self, obj):
        return obj.standard.name if obj.standard else 'Not Assigned'
    current_standard.short_description = 'Standard'

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'full_name', 'gender', 'phone_number', 'email', 'employment_type')
    list_filter = ('gender', 'employment_type', 'joining_date')
    search_fields = ('teacher_id', 'first_name', 'last_name', 'email')
    filter_horizontal = ('subjects',)
    readonly_fields = ('teacher_id',)
    exclude = ('teacher_id',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': (('first_name', 'last_name'), 'date_of_birth', 'gender', 'photo','relation_status')
        }),
        ('Contact Information', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'district', 'state', 'pin_code',('phone_number', 'email',))
        }),

        ('Employment Information', {
            'fields': ('teacher_id', 'joining_date', 'employment_type')
        }),
        ('Education', {
            'fields': ('education', 'subjects')
        }),
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'

@admin.register(Standard)
class StandardAdmin(admin.ModelAdmin):
    list_display = ('name', 'section','alias', 'class_teacher', 'class_monitor_boy', 'class_monitor_girl')
    search_fields = ('name', 'alias', 'class_teacher__first_name', 'class_teacher__last_name')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    readonly_fields = ('code',)