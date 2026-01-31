from django.urls import path
from . import views

urlpatterns = [
    # Landing page where user chooses role (student/professor)
    path('', views.home, name='home'),

    # Authentication for students
    path('login/student/', views.student_login, name='student_login'),
    path('signup/student/', views.student_signup, name='student_signup'),

    # Authentication for professors
    path('login/professor/', views.professor_login, name='professor_login'),
    path('signup/professor/', views.professor_signup, name='professor_signup'),
]
