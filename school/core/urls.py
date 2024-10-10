from django.urls import path
from .views import StudentListView, StudentDetailView, StudentCreateView, StudentUpdateView, StudentDeleteView, TeacherListView, TeacherDetailView, TeacherCreateView, TeacherUpdateView, TeacherDeleteView, \
    StandardListView, StandardDetailView, StandardCreateView, StandardUpdateView, StandardDeleteView
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login, name="login"),
    path("reset-password/", views.reset_password, name="reset-password"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.profile, name="profile"),

    ## Student URLs
    path('student/students/', StudentListView.as_view(), name='student-list'),
    path('student/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('student/create/', StudentCreateView.as_view(), name='student-create'),
    path('student/update/<int:pk>/', StudentUpdateView.as_view(), name='student-update'),
    path('student/delete/<int:pk>/', StudentDeleteView.as_view(), name='student-delete'),
    
    ## Teacher Urls
    path('teacher/teachers/', TeacherListView.as_view(), name='teacher-list'),
    path('teacher/<int:pk>/', TeacherDetailView.as_view(), name='teacher-detail'),
    path('teacher/create/', TeacherCreateView.as_view(), name='teacher-create'),
    path('teacher/update/<int:pk>/', TeacherUpdateView.as_view(), name='teacher-update'),
    path('teacher/delete/<int:pk>/', TeacherDeleteView.as_view(), name='teacher-delete'),

    ## Standard Urls
    path('standard/standards/', StandardListView.as_view(), name='standard-list'),
    path('standard/<int:pk>/', StandardDetailView.as_view(), name='standard-detail'),
    path('standard/create/', StandardCreateView.as_view(), name='standard-create'),
    path('standard/update/<int:pk>/', StandardUpdateView.as_view(), name='standard-update'),
    path('standard/delete/<int:pk>/', StandardDeleteView.as_view(), name='standard-delete'),

    ## Subjects Urls
]
