from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('join/', views.join_class, name='join_class'),
    path('class/<int:class_id>/', views.class_detail, name='class_detail'),
    path('class/<int:class_id>/leave/', views.leave_class, name='leave_class'),
    path('my-qr/', views.my_qr_code, name='my_qr_code'),
]
