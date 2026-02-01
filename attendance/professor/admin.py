from django.contrib import admin
from .models import Class, Schedule, Announcement, AttendanceRecord, AttendanceEntry, StudentClassEnrollment


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['subject', 'section', 'room', 'class_code', 'professor', 'created_at']
    list_filter = ['created_at', 'professor']
    search_fields = ['subject', 'section', 'room', 'class_code']
    readonly_fields = ['class_code']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['class_obj', 'day', 'start_time', 'end_time']
    list_filter = ['day', 'class_obj']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'class_obj', 'created_at']
    list_filter = ['created_at', 'class_obj']


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['class_obj', 'date', 'schedule_time']
    list_filter = ['date', 'class_obj']


@admin.register(AttendanceEntry)
class AttendanceEntryAdmin(admin.ModelAdmin):
    list_display = ['student', 'attendance_record', 'time_scanned']
    list_filter = ['time_scanned', 'attendance_record']


@admin.register(StudentClassEnrollment)
class StudentClassEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'class_obj', 'enrolled_at']
    list_filter = ['enrolled_at', 'class_obj']
    search_fields = ['student__username', 'class_obj__subject']
