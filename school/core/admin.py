from django.contrib import admin
from .models import Class, Subject, AcademicYear



@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'start_date', 'end_date')  # Fields to display in the admin list view
    search_fields = ('name',)  # Fields to enable search functionality
    readonly_fields = ('name','end_date')


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'section','alias', 'user', 'total_students')
    search_fields = ('name', 'alias', 'user__first_name', 'user__last_name')
    readonly_fields = ('total_students',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    readonly_fields = ('code',)