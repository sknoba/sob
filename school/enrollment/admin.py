from django.contrib import admin
from .models import Enrollment

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'academic_year', 'standard', 'enrollment_date')
    list_filter = ('academic_year', 'standard')
    search_fields = ('student__first_name', 'student__last_name', 'student__student_id')
    ordering = ('-enrollment_date',)


    
    def get_inline_instances(self, request, obj=None):
        inline_instances = super().get_inline_instances(request, obj)
        for inline in inline_instances:
            # Set the parent object for filtering
            inline.parent_object = obj
        return inline_instances