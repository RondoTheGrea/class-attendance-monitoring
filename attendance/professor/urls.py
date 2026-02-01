from django.urls import path
from . import views

app_name = 'professor'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('class/create/', views.create_class, name='create_class'),
    path('class/<int:class_id>/', views.class_detail, name='class_detail'),
    path('class/<int:class_id>/schedule/add/', views.add_schedule, name='add_schedule'),
    path('class/<int:class_id>/schedule/<int:schedule_id>/delete/', views.delete_schedule, name='delete_schedule'),
    path('class/<int:class_id>/announcement/post/', views.post_announcement, name='post_announcement'),
    path('class/<int:class_id>/qr/activate/', views.activate_qr_scanning, name='activate_qr'),
    path('class/<int:class_id>/qr/scan/', views.scan_student_qr, name='scan_student_qr'),
    path('class/<int:class_id>/qr/process/', views.process_qr_scan, name='process_qr_scan'),
    path('verify-qr/', views.verify_qr_code, name='verify_qr'),
]
