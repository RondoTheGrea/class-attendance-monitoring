from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Q
from datetime import datetime, timedelta
import json

from django.contrib.auth.models import User
from .models import Class, Schedule, Announcement, AttendanceRecord, AttendanceEntry, StudentClassEnrollment
from .forms import ClassForm, ScheduleForm, AnnouncementForm


def get_active_schedule(class_obj, current_time=None):
    """Helper function to get the active schedule for a class at the given time"""
    if current_time is None:
        from django.utils import timezone
        current_time = timezone.now()
    
    current_day = current_time.strftime('%A')
    time_only = current_time.time() if hasattr(current_time, 'time') else current_time
    
    for schedule in class_obj.schedules.filter(day=current_day):
        if schedule.start_time <= time_only <= schedule.end_time:
            return schedule
    return None


@login_required
def dashboard(request):
    """Main dashboard showing all classes for the professor"""
    classes = Class.objects.filter(professor=request.user).annotate(
        schedule_count=Count('schedules'),
        announcement_count=Count('announcements'),
        attendance_count=Count('attendance_records')
    )

    context = {
        'classes': classes,
    }
    return render(request, 'professor/dashboard.html', context)


@login_required
def class_detail(request, class_id):
    """Class detail view with tabs for overview, schedule, announcements, and attendance"""
    class_obj = get_object_or_404(Class, id=class_id, professor=request.user)
    
    # Get active tab from query parameter
    active_tab = request.GET.get('tab', 'overview')
    
    # Get schedules
    schedules = class_obj.schedules.all()
    
    # Get announcements
    announcements = class_obj.announcements.all()
    
    # Get attendance records
    attendance_records = class_obj.attendance_records.all()
    
    # Calculate stats
    total_students = class_obj.get_total_students()
    total_sessions = class_obj.get_total_sessions()
    
    context = {
        'class_obj': class_obj,
        'schedules': schedules,
        'announcements': announcements,
        'attendance_records': attendance_records,
        'active_tab': active_tab,
        'total_students': total_students,
        'total_sessions': total_sessions,
    }
    
    return render(request, 'professor/class_detail.html', context)


@login_required
def create_class(request):
    """Create a new class"""
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            class_obj = form.save(commit=False)
            class_obj.professor = request.user
            class_obj.save()
            messages.success(request, f'Class "{class_obj.subject}" created successfully!')
            return redirect('professor:dashboard')
    else:
        form = ClassForm()
    
    return render(request, 'professor/create_class_modal.html', {'form': form})


@login_required
def add_schedule(request, class_id):
    """Add a schedule to a class"""
    class_obj = get_object_or_404(Class, id=class_id, professor=request.user)
    
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.class_obj = class_obj
            
            # Check for conflicts
            existing_schedules = Schedule.objects.filter(
                class_obj=class_obj,
                day=schedule.day
            )
            
            start_minutes = schedule.start_time.hour * 60 + schedule.start_time.minute
            end_minutes = schedule.end_time.hour * 60 + schedule.end_time.minute
            
            for existing in existing_schedules:
                existing_start = existing.start_time.hour * 60 + existing.start_time.minute
                existing_end = existing.end_time.hour * 60 + existing.end_time.minute
                
                if (start_minutes >= existing_start and start_minutes < existing_end) or \
                   (end_minutes > existing_start and end_minutes <= existing_end) or \
                   (start_minutes <= existing_start and end_minutes >= existing_end):
                    messages.error(request, 'This schedule conflicts with an existing schedule on the same day.')
                    return redirect('professor:class_detail', class_id=class_id)
            
            schedule.save()
            messages.success(request, 'Schedule added successfully!')
            return redirect('professor:class_detail', class_id=class_id)
    else:
        form = ScheduleForm()
    
    return redirect('professor:class_detail', class_id=class_id)


@login_required
def delete_schedule(request, class_id, schedule_id):
    """Delete a schedule"""
    class_obj = get_object_or_404(Class, id=class_id, professor=request.user)
    schedule = get_object_or_404(Schedule, id=schedule_id, class_obj=class_obj)
    schedule.delete()
    messages.success(request, 'Schedule deleted successfully!')
    return redirect('professor:class_detail', class_id=class_id)


@login_required
def post_announcement(request, class_id):
    """Post a new announcement"""
    class_obj = get_object_or_404(Class, id=class_id, professor=request.user)
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.class_obj = class_obj
            announcement.save()
            messages.success(request, 'Announcement posted successfully!')
            return redirect('professor:class_detail', class_id=class_id)
    else:
        form = AnnouncementForm()
    
    return redirect('professor:class_detail', class_id=class_id)


@login_required
def activate_qr_scanning(request, class_id):
    """Activate QR code scanning for a class session"""
    class_obj = get_object_or_404(Class, id=class_id, professor=request.user)
    
    # Check if class has schedules
    schedules = class_obj.schedules.all()
    if not schedules.exists():
        messages.error(request, 'Please configure class schedules first before activating QR scanning.')
        return redirect('professor:class_detail', class_id=class_id)
    
    # Check if current time matches any schedule
    now = timezone.now()
    current_day = now.strftime('%A')
    current_time = now.time()
    
    active_schedule = None
    for schedule in schedules:
        if schedule.day == current_day:
            if schedule.start_time <= current_time <= schedule.end_time:
                active_schedule = schedule
                break
    
    if not active_schedule:
        messages.error(request, 'This class is not scheduled for the current time. QR scanning is only available during scheduled class hours.')
        return redirect('professor:class_detail', class_id=class_id)
    
    # Generate QR code data
    qr_data = {
        'classId': str(class_obj.id),
        'className': class_obj.subject,
        'professorId': str(request.user.id),
        'timestamp': now.isoformat()
    }
    
    # Create or get attendance record for this session
    schedule_time_str = f"{active_schedule.start_time.strftime('%H:%M')} - {active_schedule.end_time.strftime('%H:%M')}"
    
    # Check if there's already an attendance record for today's session
    attendance_record, created = AttendanceRecord.objects.get_or_create(
        class_obj=class_obj,
        date__date=now.date(),
        schedule_time=schedule_time_str,
        defaults={
            'date': now,
            'qr_code_data': json.dumps(qr_data)
        }
    )
    
    if not created:
        attendance_record.qr_code_data = json.dumps(qr_data)
        attendance_record.save()
    
    context = {
        'class_obj': class_obj,
        'qr_data': qr_data,
        'qr_data_json': json.dumps(qr_data),
        'schedule_time': schedule_time_str,
    }
    
    return render(request, 'professor/qr_code_modal.html', context)


@login_required
def verify_qr_code(request):
    """Verify QR code and mark attendance (for students to call)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            qr_data = json.loads(data.get('qr_code_data', '{}'))
            
            class_id = qr_data.get('classId')
            timestamp_str = qr_data.get('timestamp')
            
            if not class_id or not timestamp_str:
                return JsonResponse({'success': False, 'error': 'Invalid QR code data'}, status=400)
            
            # Verify timestamp (QR code should be valid for current session)
            qr_timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            now = timezone.now()
            
            # Check if QR code is not too old (within 2 hours)
            if (now - qr_timestamp).total_seconds() > 7200:
                return JsonResponse({'success': False, 'error': 'QR code has expired'}, status=400)
            
            # Get class and verify
            class_obj = get_object_or_404(Class, id=class_id)
            
            # Find the attendance record
            attendance_record = AttendanceRecord.objects.filter(
                class_obj=class_obj,
                qr_code_data__contains=qr_data.get('timestamp', '')
            ).order_by('-date').first()
            
            if not attendance_record:
                return JsonResponse({'success': False, 'error': 'Attendance session not found'}, status=404)
            
            # Check if student already marked attendance
            if AttendanceEntry.objects.filter(
                attendance_record=attendance_record,
                student=request.user
            ).exists():
                return JsonResponse({'success': False, 'error': 'Attendance already marked'}, status=400)
            
            # Create attendance entry
            AttendanceEntry.objects.create(
                attendance_record=attendance_record,
                student=request.user
            )
            
            return JsonResponse({'success': True, 'message': 'Attendance marked successfully'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


@login_required
def scan_student_qr(request, class_id):
    """Professor view to scan student QR codes"""
    class_obj = get_object_or_404(Class, id=class_id, professor=request.user)
    
    # Check if class has schedules
    if not class_obj.schedules.exists():
        messages.error(request, 'Please configure class schedules first before scanning QR codes.')
        return redirect('professor:class_detail', class_id=class_id)
    
    # Check if current time matches any schedule
    now = timezone.now()
    active_schedule = get_active_schedule(class_obj, now)
    
    if not active_schedule:
        messages.error(request, 'This class is not scheduled for the current time. QR scanning is only available during scheduled class hours.')
        return redirect('professor:class_detail', class_id=class_id)
    
    # Create or get attendance record for this session
    schedule_time_str = f"{active_schedule.start_time.strftime('%H:%M')} - {active_schedule.end_time.strftime('%H:%M')}"
    
    attendance_record, created = AttendanceRecord.objects.get_or_create(
        class_obj=class_obj,
        date__date=now.date(),
        schedule_time=schedule_time_str,
        defaults={
            'date': now,
        }
    )
    
    context = {
        'class_obj': class_obj,
        'attendance_record': attendance_record,
        'schedule_time': schedule_time_str,
    }
    
    return render(request, 'professor/scan_qr.html', context)


@login_required
def process_qr_scan(request, class_id):
    """Process scanned student QR code and mark attendance"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            scanned_name = data.get('student_name', '').strip()
            
            if not scanned_name:
                return JsonResponse({'success': False, 'error': 'No student name provided'}, status=400)
            
            # Get the class
            class_obj = get_object_or_404(Class, id=class_id, professor=request.user)
            
            # Search for students enrolled in this class whose full name matches
            enrollments = StudentClassEnrollment.objects.filter(class_obj=class_obj).select_related('student')
            
            matching_student = None
            for enrollment in enrollments:
                student = enrollment.student
                student_full_name = student.get_full_name() or student.username
                if student_full_name.strip().lower() == scanned_name.lower():
                    matching_student = student
                    break
            
            if not matching_student:
                return JsonResponse({
                    'success': False, 
                    'error': f'No enrolled student found with name "{scanned_name}"'
                }, status=404)
            
            # Get or create attendance record for today's session
            now = timezone.now()
            active_schedule = get_active_schedule(class_obj, now)
            
            if not active_schedule:
                return JsonResponse({
                    'success': False, 
                    'error': 'No active schedule found for current time'
                }, status=400)
            
            schedule_time_str = f"{active_schedule.start_time.strftime('%H:%M')} - {active_schedule.end_time.strftime('%H:%M')}"
            
            attendance_record, _ = AttendanceRecord.objects.get_or_create(
                class_obj=class_obj,
                date__date=now.date(),
                schedule_time=schedule_time_str,
                defaults={
                    'date': now,
                }
            )
            
            # Check if student already marked attendance for this session
            if AttendanceEntry.objects.filter(
                attendance_record=attendance_record,
                student=matching_student
            ).exists():
                return JsonResponse({
                    'success': False, 
                    'error': f'Attendance already marked for {matching_student.get_full_name() or matching_student.username}'
                }, status=400)
            
            # Create attendance entry
            AttendanceEntry.objects.create(
                attendance_record=attendance_record,
                student=matching_student
            )
            
            return JsonResponse({
                'success': True, 
                'message': f'Attendance marked for {matching_student.get_full_name() or matching_student.username}',
                'student_name': matching_student.get_full_name() or matching_student.username
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)