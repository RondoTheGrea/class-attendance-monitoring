from django.urls import path
from . import views

app_name = 'professor'

urlpatterns = [
    # professor-only pages after authentication
    path('dashboard/', views.dashboard, name='dashboard'),
]
