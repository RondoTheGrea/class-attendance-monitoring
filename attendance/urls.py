"""
URL configuration for attendance project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('student/', include('student.urls')),
    path('professor/', include('professor.urls')),
]
