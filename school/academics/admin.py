from django.contrib import admin
from .models import Exams, ExamScore, TimeTable, TeacherTest, TestScoring
from django.utils.html import format_html
from simple_history.admin import SimpleHistoryAdmin

# Custom admin class for the Exams model
class ExamsAdmin(SimpleHistoryAdmin):
    list_display = ('exam', 'class_name', 'academic_year', 'start_date', 'end_date', 'result_date')
    search_fields = ('exam', 'academic_year', 'class_name__name')  # Search by exam and class_name
    list_filter = ('exam', 'academic_year', 'start_date', 'end_date', 'class_name')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)

# Custom admin class for the ExamScore model
class ExamScoreAdmin(SimpleHistoryAdmin):
    list_display = ('exam', 'subject', 'student', 'theory_marks', 'slip_test_marks', 'seminar_marks', 'note_book_keeping_marks', 'subject_enrichment')
    search_fields = ('exam__exam', 'subject__name', 'student__user__username')  # Search by exam, subject, and student
    list_filter = ('exam', 'subject', 'student')
    ordering = ('-exam__start_date',)

# Register the models with custom admin
admin.site.register(Exams, ExamsAdmin)
admin.site.register(ExamScore, ExamScoreAdmin)



class TimeTableAdmin(SimpleHistoryAdmin):
    list_display = ('exam', 'subject', 'date', 'duration', 'info', 'formatted_date')
    search_fields = ('exam__exam', 'subject__name')
    list_filter = ('exam', 'subject')
    date_hierarchy = 'date'
    ordering = ('date',)

    # Display formatted date in a more readable format
    def formatted_date(self, obj):
        return obj.date.strftime('%Y-%m-%d %H:%M:%S')
    formatted_date.short_description = 'Formatted Date'


class TeacherTestAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'class_name', 'subjects', 'taken_by', 'date', 'duration', 'total_marks')
    search_fields = ('name', 'class_name__name', 'subjects__name', 'taken_by__username')
    list_filter = ('class_name', 'subjects', 'taken_by')
    date_hierarchy = 'date'
    ordering = ('date',)
    # filter_horizontal = ('subjects',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Optionally filter queryset based on user type or other conditions
        return queryset


class TestScoringAdmin(SimpleHistoryAdmin):
    list_display = ('test', 'student', 'obtain_mark', 'result')
    search_fields = ('test__name', 'student__student__first_name', 'student__student__last_name')
    list_filter = ('test', 'result')
    ordering = ('test__date',)

    def student_name(self, obj):
        return format_html('<b>{}</b>', obj.student.student.first_name)
    student_name.short_description = 'Student Name'



admin.site.register(TimeTable, TimeTableAdmin)
admin.site.register(TeacherTest, TeacherTestAdmin)
admin.site.register(TestScoring, TestScoringAdmin)


# class TimeTableInline(admin.TabularInline):
#     model = TimeTable
#     extra = 1  # Show one empty form initially


# class TeacherTestAdmin(SimpleHistoryAdmin):
#     list_display = ('name', 'class_name', 'subjects', 'taken_by', 'date', 'duration', 'total_marks')
#     search_fields = ('name', 'class_name__name', 'subjects__name', 'taken_by__username')
#     list_filter = ('class_name', 'subjects', 'taken_by')
#     date_hierarchy = 'date'
#     ordering = ('date',)
#     filter_horizontal = ('subjects',)
#     inlines = [TimeTableInline]  # Add the inline model

