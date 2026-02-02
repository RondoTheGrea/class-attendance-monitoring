from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import secrets
import string


def generate_class_code():
    """Generate a unique 6-character class code"""
    characters = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(secrets.choice(characters) for _ in range(6))
        if not Class.objects.filter(class_code=code).exists():
            return code


class Class(models.Model):
    """Represents a class taught by a professor"""
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classes')
    subject = models.CharField(max_length=200)
    section = models.CharField(max_length=50, blank=True, null=True)
    room = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True, max_length=500)
    class_code = models.CharField(max_length=6, unique=True, blank=True, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.class_code:
            self.class_code = generate_class_code()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Classes"
        ordering = ['-created_at']

    def __str__(self):
        if self.section:
            return f"{self.subject} - Section {self.section}"
        return self.subject

    def get_total_students(self):
        """Get total enrolled students count"""
        return self.enrolled_students.count()

    def get_total_sessions(self):
        """Get total number of attendance sessions"""
        return AttendanceRecord.objects.filter(class_obj=self).count()


class Schedule(models.Model):
    """Represents a weekly schedule for a class"""
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='schedules')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['day', 'start_time']
        unique_together = ['class_obj', 'day', 'start_time', 'end_time']

    def __str__(self):
        return f"{self.class_obj.subject} - {self.day} {self.start_time} - {self.end_time}"


class ExtraClass(models.Model):
    """Represents a one-time extra class session (makeup class, special session, etc.)"""
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='extra_classes')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    reason = models.CharField(max_length=200, blank=True, null=True)  # e.g., "Makeup class", "Review session"
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['class_obj', 'date', 'start_time', 'end_time']

    def __str__(self):
        return f"{self.class_obj.subject} - {self.date} {self.start_time} - {self.end_time}"


class Announcement(models.Model):
    """Represents an announcement posted by a professor for a class"""
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.class_obj.subject} - {self.title}"


class AttendanceRecord(models.Model):
    """Represents a single attendance session for a class"""
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateTimeField(default=timezone.now)
    schedule_time = models.CharField(max_length=50)  # e.g., "09:00 - 10:30"
    qr_code_data = models.TextField(blank=True, null=True)  # Store QR code JSON data
    canceled = models.BooleanField(default=False)  # Whether the class was canceled

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.class_obj.subject} - {self.date.strftime('%Y-%m-%d %H:%M')}"

    def get_student_count(self):
        """Get number of students who attended this session"""
        return self.entries.count()


class AttendanceEntry(models.Model):
    """Represents a single student's attendance entry"""
    attendance_record = models.ForeignKey(AttendanceRecord, on_delete=models.CASCADE, related_name='entries')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_entries')
    time_scanned = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['attendance_record', 'student']
        ordering = ['time_scanned']

    def __str__(self):
        return f"{self.student.username} - {self.attendance_record}"


class StudentClassEnrollment(models.Model):
    """Tracks which students are enrolled in which classes"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrolled_classes')
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='enrolled_students')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'class_obj']
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.student.username} - {self.class_obj.subject}"
