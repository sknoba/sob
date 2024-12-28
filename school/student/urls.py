from django.urls import path
from .views import *
from .export_utils import *


urlpatterns = [
    path("test", test, name="test"),
    path('dashboard', EnrollmentDashboardView.as_view(), name='enrollment-dashboard'), #enrollment dashboard
    path('students/', StudentListView.as_view(), name='student-list'), #all students

    path('enroll/step1', StudentFormStep1View.as_view(), name='enroll_step1'),
    path('enroll/<int:student_id>/step2', StudentFormStep2View.as_view(), name='enroll_step2'),
    path('enroll/<int:student_id>/step3', EnrollmentCreateView.as_view(), name='enroll_step3'), #enroll student
    path('enroll/<int:enroll_id>/step4', EnrollmentFeesView.as_view(), name='enroll_step4'), #enroll student
    path('enroll/<int:enroll_id>/done', EnrollmentDoneView.as_view(), name='enrollment-done'), 
    path('enrollments/', EnrollmentlistView.as_view(), name='enrollment-list'), #all students
    path('promots/', StudentPromoteListView.as_view(), name='promote-list'), #all students

    path('<int:id>/detail', StudentDetailView.as_view(), name='student-detail'),
    path('<int:pk>/update', StudentUpdateView.as_view(), name='student-update'),


    path('enroll/<int:id>/detail', EnrollmentDetailView.as_view(), name='enrollment-detail'), #enroll student

    
    # path('enrollment-list/', EnrollmentlistView.as_view(), name='enrollment-list'), #all enrollments    
    # path('enrollment-student-list/', StudentListView.as_view(), name='enrollment-student-list'), #all enrollments    
    path('enrollment-cancel-list/', EnrollmentCancelListView.as_view(), name='enrollment-cancel-list'), #all enrollments    
    
    # path('enroll/<int:id>/fees', EnrollmentFeesView.as_view(), name='enrollment-fees'), #define fees
    

    # PDF Generate URLs
    path("<int:id>/enrollment_form", GenerateStudentPDF.as_view(), name="enrollment_form"),
    path("<int:id>/enrollment_recipt", AddmissionReciptPdf.as_view(), name="admission_receipt"),

    

    ## Student URLs
    
    path('archives/students/', StudentArchiveListView.as_view(), name='student-archive-list'),
    #done enrollment
    # path('<int:pk>/delete', StudentDeleteView.as_view(), name='student-delete'),
]