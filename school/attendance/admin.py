from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Attendance, AttendaceRecord

# from .models import Attendance

# @admin.register(Attendance)
# class AttendanceAdmin(admin.ModelAdmin):
#     list_display = ('id', 'student', 'date', 'status', 'created_by',)
#     search_fields = ('student__name', 'student__roll_no', 'date')
#     list_filter = ('status', 'date')
#     ordering = ('-date',)
#     autocomplete_fields = ('student', 'created_by')  # Autocomplete for foreign keys
#     fieldsets = (
#         # (None, {
#         #     'fields': ('student', 'date', 'status')
#         # }),
#         ('Attendance Information', {
#             'fields': ('student','status', 'created_by',   'date'),
#         }),
#     )
#     readonly_fields = ('date',)  # Prevent manual changes


# @admin.register(Attendance)
# class AttendanceAdmin(SimpleHistoryAdmin):
#     list_display = ('a_class', 'date', 'created_by', 'total', 'present', 'absent')
#     list_filter = ('a_class', 'date')
#     search_fields = ('a_class__name', 'created_by__username')
#     ordering = ('-date',)

#     # Customize the admin form
#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         if not request.user.is_superuser:
#             form.base_fields['created_by'].queryset = form.base_fields['created_by'].queryset.filter(username=request.user)
#         return form
    
# @admin.register(AttendaceRecord)
# class AttendanceRecordAdmin(SimpleHistoryAdmin):
#     list_display = ('student', 'attendance', 'status')
#     list_filter = ('status', 'attendance__a_class', 'attendance__date')
#     search_fields = ('student__name', 'attendance__a_class__name', 'status')
#     ordering = ('-attendance__date',)

#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         if not request.user.is_superuser:
#             form.base_fields['student'].queryset = form.base_fields['student'].queryset.filter(user=request.user)
#         return form


# class AttendanceRecordInline(admin.TabularInline):
#     model = AttendaceRecord
#     extra = 1  # Number of empty forms to display for new records
#     can_delete = True
#     fields = ('student', 'status')  # Fields to display in the inline form
#     readonly_fields = ('attendance',)  # Make attendance read-only (optional)

# @admin.register(Attendance)
# class AttendanceAdmin(SimpleHistoryAdmin):
#     list_display = ('a_class', 'date', 'created_by', 'total', 'present', 'absent')
#     list_filter = ('a_class', 'date')
#     search_fields = ('a_class__name', 'created_by__username')
#     ordering = ('-date',)
#     inlines = [AttendanceRecordInline]  # Attach the inline

#     # Customize the admin form
#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         if not request.user.is_superuser:
#             form.base_fields['created_by'].queryset = form.base_fields['created_by'].queryset.filter(username=request.user)
#         return form

class AttendanceRecordInline(admin.TabularInline):
    model = AttendaceRecord
    extra = 1  # Number of empty forms to display for new records
    can_delete = True
    fields = ('student', 'status')  # Fields to display in the inline form
    readonly_fields = ('attendance',)  # Make attendance read-only (optional)

@admin.register(Attendance)
class AttendanceAdmin(SimpleHistoryAdmin):
    list_display = ('class_name', 'date', 'user', 'present', 'absent')
    list_filter = ('class_name', 'date')
    search_fields = ('class_name__name', 'user__username__first_name')
    ordering = ('-date',)
    inlines = [AttendanceRecordInline]  # Attach the inline

    # Customize the admin form
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['user'].queryset = form.base_fields['user'].queryset.filter(username=request.user)
        return form

@admin.register(AttendaceRecord)
class AttendanceRecordAdmin(SimpleHistoryAdmin):
    list_display = ('attendance', 'student', 'status')
    list_filter = ('attendance__date', 'status', 'attendance__class_name')
    search_fields = ('attendance__class_name__name', 'student__name')
    ordering = ('attendance__date',)