from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard', EnrollmentDashboardView.as_view(), name='enrollment-dashboard'), #enrollment dashboard
    path('enrollment-list/', EnrollmentlistView.as_view(), name='enrollment-list'), #all enrollments    
    path('enrollment-student-list/', StudentListView.as_view(), name='enrollment-student-list'), #all enrollments    
    path('enrollment-cancel-list/', EnrollmentCancelListView.as_view(), name='enrollment-cancel-list'), #all enrollments    
    path('enroll/<int:id>/detail', EnrollmentDetailView.as_view(), name='enrollment-detail'), #enroll student
    path('enroll/<int:id>/enroll', EnrollmentCreateView.as_view(), name='enroll'), #enroll student
    path('enroll/<int:id>/fees', EnrollmentFeesView.as_view(), name='enrollment-fees'), #define fees
    path('enroll/<int:id>/done', EnrollmentDoneView.as_view(), name='enrollment-done'), #done enrollment
]