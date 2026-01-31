from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    # student-only pages after authentication
    path('dashboard/', views.dashboard, name='dashboard'),
]
