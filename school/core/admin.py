from django.contrib import admin
from .models import Student, Standard, UserProfile, Subject, AcademicYear



@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name','is_active', 'start_date', 'end_date')
    search_fields = ('name',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id','full_name', 'gender', 'date_of_birth', 'create_date')
    list_filter = ('gender', 'create_date')
    search_fields = ('student_id', 'first_name', 'last_name', 'father_name', 'mother_name')
    readonly_fields = ('create_date','student_id')
    exclude = ('student_id',)

    
    fieldsets = (
        ('Personal Information', {
            'fields': (('first_name', 'last_name'), 'date_of_birth', 'gender', 'photo')
        }),
        ('Academic Information', {
            'fields': ('is_active','student_id')
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
   


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('acc_id', 'user', 'acc_type','gender', 'phone_number', 'employment_type')
    list_filter = ('gender', 'employment_type', 'acc_type')
    search_fields = ('acc_id',)
    filter_horizontal = ('subjects',)
    readonly_fields = ('acc_id',)
    exclude = ('acc_id',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('date_of_birth', 'gender', 'photo','relation_status')
        }),
        ('Contact Information', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'district', 'state', 'pin_code',('phone_number',))
        }),

        ('Employment Information', {
            'fields': ('acc_type','acc_id', 'employment_type')
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