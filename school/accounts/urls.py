from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login", auth_views.LoginView.as_view(template_name='accounts/login.html',redirect_authenticated_user=True), name="login"),
    path("reset-password", auth_views.PasswordResetView.as_view(template_name='accounts/passwordreset.html'), name="reset-password"),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
    path("profile", ProfileView.as_view(), name="profile"),

    ## AccessMangement
  
    path('manage-access/teacher-register', TeacherRegisterView.as_view(), name='access-teacher-register'),
    path('manage-access/staff-register', StaffRegisterView.as_view(), name='access-staff-register'),
    path('manage-access/<int:user_id>/user-access', UserCreateAccessView.as_view(), name='access-user-access'),

    path('manage-access/user-list/', UserListView.as_view(), name='access-user-list'),      
    path('manage-access/user-teacher', UserTeacherListView.as_view(), name='access-user-teacher'),    
    path('manage-access/user-staff', UserStaffListView.as_view(), name='access-user-staff'),
    path('manage-access/<int:user_id>/user-detail', UserDetailView.as_view(), name='access-user-detail'),
    path('manage-access/<int:user_id>/profile-update', UserProfileUpdateView.as_view(), name='access-profile-update'),  


    path('manage-access/', views.accessmanagement, name='manage-access'),
    
    path('manage-access/<int:user_id>/user-access-update', UserAccessUpdateView.as_view(), name='access-user-access-update'),
    
    path('manage-access/<int:user_id>/user-delete', UserDeleteView.as_view(), name='access-user-delete'),    
    # Group Urls

    path('manage-access/group-list/', GroupListView.as_view(), name='access-group-list'),
    path('manage-access/group-create', GroupCreateView.as_view(), name='access-group-create'),
    path('manage-access/<int:pk>/group-update', GroupUpdateView.as_view(), name='access-group-update'),
    path('manage-access/<int:pk>/group-delete', GroupDeleteView.as_view(), name='access-group-delete'),    

    # # ## Teacher Urls
    # path('teacher/teachers/', TeacherListView.as_view(), name='teacher-list'),
    # path('teacher/<str:acc_id>/detail', TeacherDetailView.as_view(), name='teacher-detail'),
    # path('teacher/<str:acc_id>/update', TeacherUpdateView.as_view(), name='teacher-update'),

    # # ## Staff Urls
    # path('staff/staffs/', StaffListView.as_view(), name='staff-list'),
    # path('staff/<str:acc_id>/detail', StaffDetailView.as_view(), name='staff-detail'),
    # path('staff/<str:acc_id>/update', StaffUpdateView.as_view(), name='staff-update'),
]