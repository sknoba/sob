from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

handler403 = 'accounts.views.custom_403_view'

urlpatterns = [
    path('webpush/', include('webpush.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('core.urls')),
    path('student/', include('student.urls')),
    path('attendance/', include('attendance.urls')),
    path('fees/', include('school_fees.urls')),
    path('academic/', include('academics.urls')),
  
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)