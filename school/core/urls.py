from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .export_util import GenerateStudentPDF
from django.contrib.auth import views as auth_views

# app_name = 'core'

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login", auth_views.LoginView.as_view(template_name='core/login.html',redirect_authenticated_user=True), name="login"),
    path("reset-password", auth_views.PasswordResetView.as_view(template_name='core/passwordreset.html'), name="reset-password"),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
    path("profile", views.profile, name="profile"),

    ## PDF Generate URLs
    path("student/enrollment/pdf/<int:id>/", GenerateStudentPDF.as_view(), name="generate_pdf"),

    ## Student URLs
    path('student/students/', StudentListView.as_view(), name='student-list'),
    path('student/archives/students/', StudentArchiveListView.as_view(), name='student-archive-list'),
    path('student/create/', StudentCreateView.as_view(), name='student-create'),
    path('student/<int:id>/detail', StudentDetailView.as_view(), name='student-detail'),
    path('student/<int:pk>/update', StudentUpdateView.as_view(), name='student-update'),
    path('student/<int:pk>/delete', StudentDeleteView.as_view(), name='student-delete'),
    
    # ## Teacher Urls
    path('teacher/teachers/', TeacherListView.as_view(), name='teacher-list'),
    path('teacher/<str:acc_id>/detail', TeacherDetailView.as_view(), name='teacher-detail'),
    path('teacher/<str:acc_id>/update', TeacherUpdateView.as_view(), name='teacher-update'),

    # ## Staff Urls
    path('staff/staffs/', StaffListView.as_view(), name='staff-list'),
    path('staff/<str:acc_id>/detail', StaffDetailView.as_view(), name='staff-detail'),
    path('staff/<str:acc_id>/update', StaffUpdateView.as_view(), name='staff-update'),

    ## Staff Urls    

    # ## Standard Urls
    path('standard/standards/', StandardListView.as_view(), name='standard-list'),
    path('standard/<int:pk>/detail', StandardDetailView.as_view(), name='standard-detail'),
    path('standard/create', StandardCreateView.as_view(), name='standard-create'),
    path('standard/<int:pk>/update', StandardUpdateView.as_view(), name='standard-update'),
    path('standard/<int:pk>/delete', StandardDeleteView.as_view(), name='standard-delete'),

    ## AccessMangement
    path('manage-access/', views.accessmanagement, name='manage-access'),
    path('manage-access/user-list/', UserListView.as_view(), name='access-user-list'),    
    path('manage-access/user-register', UserRegisterView.as_view(), name='access-user-register'),    
    path('manage-access/<int:user_id>/user-access', UserCreateAccessView.as_view(), name='access-user-access'),
    path('manage-access/<int:user_id>/user-access-update', UserAccessUpdateView.as_view(), name='access-user-access-update'),
    path('manage-access/<int:user_id>/user-update', UserProfileUpdateView.as_view(), name='access-user-update'),  
    path('manage-access/<int:user_id>/user-delete', UserDeleteView.as_view(), name='access-user-delete'),
    ## Group Urls
    path('manage-access/group-list/', GroupListView.as_view(), name='access-group-list'),
    path('manage-access/group-create', GroupCreateView.as_view(), name='access-group-create'),
    path('manage-access/<int:pk>/group-update', GroupUpdateView.as_view(), name='access-group-update'),
    path('manage-access/<int:pk>/group-delete', GroupDeleteView.as_view(), name='access-group-delete'),



    ## Academic Year Urls
    path('academic-year/', views.AcademicYearListView.as_view(), name='academic-year-list'),
    path('academic-year/<int:pk>/detail', views.AcademicYearDetailView.as_view(), name='academic-year-detail'),
    path('academic-year/add/', views.AcademicYearCreateView.as_view(), name='academic-year-add'),
    path('academic-year<int:pk>/edit', views.AcademicYearUpdateView.as_view(), name='academic-year-edit'),
    path('academic-year/<int:pk>/delete', views.AcademicYearDeleteView.as_view(), name='academic-year-delete'),


    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)