from django.urls import path
from .views import *

urlpatterns = [
    path('students/', StudentListView.as_view(), name='student-list'),
    path('student/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('student/create/', StudentCreateView.as_view(), name='student-create'),
    path('student/update/<int:pk>/', StudentUpdateView.as_view(), name='student-update'),
    path('student/delete/<int:pk>/', StudentDeleteView.as_view(), name='student-delete'),
]
