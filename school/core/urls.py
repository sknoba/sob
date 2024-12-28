from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# app_name = 'core'

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    
    # # ## Standard Urls
    path('class/classes/', ClassView.as_view(), name='classes-list'),
    path('class/<int:pk>/detail', StandardDetailView.as_view(), name='class-detail'),    
    path('class/<int:pk>/update', StandardUpdateView.as_view(), name='standard-update'),
    # path('class/<int:pk>/delete', StandardDeleteView.as_view(), name='standard-delete'),

    # ## Academic Year Urls
    path('academic-year/', views.AcademicYearView.as_view(), name='academic-year-list'),
    path('academic-year/<int:pk>/detail', views.AcademicYearDetailView.as_view(), name='academic-year-detail'),    
    path('academic-year<int:pk>/edit', views.AcademicYearUpdateView.as_view(), name='academic-year-edit'),
    path('academic-year/<int:pk>/delete', views.AcademicYearDeleteView.as_view(), name='academic-year-delete'),

    # ## Academic Year Urls
    path('subjects/', views.SubjectView.as_view(), name='subject-list'),
    path('subject/<int:pk>/detail', views.SubjectDetailView.as_view(), name='subject-detail'),
    # path('academic-year/<int:pk>/detail', views.AcademicYearDetailView.as_view(), name='academic-year-detail'),    
    # path('academic-year<int:pk>/edit', views.AcademicYearUpdateView.as_view(), name='academic-year-edit'),
    # path('academic-year/<int:pk>/delete', views.AcademicYearDeleteView.as_view(), name='academic-year-delete'),
    

    # Notification Urls
    path('vapid-config', vapid_config_js, name='vapid_config_js'),
    path('webpush/save_subscription/', save_subscription, name='save_subscription'),
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)