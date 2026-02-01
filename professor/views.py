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
    # Get active tab from query parameter (defaults to 'classes')
    active_tab = request.GET.get('tab', 'classes')
    
    classes = Class.objects.filter(professor=request.user).annotate(
        schedule_count=Count('schedules'),
        announcement_count=Count('announcements'),
        attendance_count=Count('attendance_records')
    )

    context = {
        'classes': classes,
        'active_tab': active_tab,
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
    
    # Calculate average attendance rate
    attendance_rate = 0
    if total_students > 0 and total_sessions > 0:
        total_possible = total_students * total_sessions
        # AttendanceEntry records mean the student was present (scanned QR)
        total_present = AttendanceEntry.objects.filter(
            attendance_record__class_obj=class_obj
        ).count()
        attendance_rate = round((total_present / total_possible) * 100) if total_possible > 0 else 0
    
    context = {
        'class_obj': class_obj,
        'schedules': schedules,
        'announcements': announcements,
        'attendance_records': attendance_records,
        'active_tab': active_tab,
        'total_students': total_students,
        'total_sessions': total_sessions,
        'attendance_rate': attendance_rate,
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
def edit_class(request, class_id):
    """Edit an existing class (subject, section, room, description)."""
    class_obj = get_object_or_404(Class, id=class_id, professor=request.user)

    if request.method == 'POST':
        form = ClassForm(request.POST, instance=class_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Class "{class_obj.subject}" updated successfully!')
            return redirect('professor:dashboard')
    else:
        form = ClassForm(instance=class_obj)

    return render(request, 'professor/edit_class_modal.html', {'form': form, 'class_obj': class_obj})


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
    """Activate QR scanning for a class session and open the scanner.

    This ensures there is an active schedule (Asia/Manila local time) and
    that an AttendanceRecord exists for the current session, then sends
    the professor to the camera scanner page.
    """
    class_obj = get_object_or_404(Class, id=class_id, professor=request.user)
    
    # Check if class has schedules
    schedules = class_obj.schedules.all()
    if not schedules.exists():
        messages.error(request, 'Please configure class schedules first before activating QR scanning.')
        return redirect('professor:class_detail', class_id=class_id)
    
    # Check if current time matches any schedule (use Asia/Manila local time)
    now = timezone.localtime(timezone.now(), timezone.get_default_timezone())
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

    # Ensure an attendance record exists for this session
    schedule_time_str = f"{active_schedule.start_time.strftime('%H:%M')} - {active_schedule.end_time.strftime('%H:%M')}"

    AttendanceRecord.objects.get_or_create(
        class_obj=class_obj,
        date__date=now.date(),
        schedule_time=schedule_time_str,
        defaults={
            'date': now,
        }
    )

    # Redirect directly to the scanner page
    return redirect('professor:scan_student_qr', class_id=class_obj.id)


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
    """Professor view to scan student QR codes using the camera.

    Only available when there is an active schedule for this class right now.
    """
    class_obj = get_object_or_404(Class, id=class_id, professor=request.user)

    # Require schedules
    if not class_obj.schedules.exists():
        messages.error(request, 'Please configure class schedules first before scanning QR codes.')
        return redirect('professor:class_detail', class_id=class_id)

    # Require an active schedule for the current date/time (Asia/Manila local time)
    now = timezone.localtime(timezone.now(), timezone.get_default_timezone())
    active_schedule = get_active_schedule(class_obj, now)

    if not active_schedule:
        messages.error(request, 'This class is not scheduled for the current time. QR scanning is only available during scheduled class hours.')
        return redirect('professor:class_detail', class_id=class_id)

    # Ensure there is an attendance record for this session
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
    """Process a scanned student QR code and mark attendance.

    The student QR encodes the student's full name (or username fallback).
    We match that name against enrollments for this class and append an
    AttendanceEntry to the current session's AttendanceRecord.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body or '{}')
        scanned_name = (data.get('student_name') or '').strip()

        if not scanned_name:
            return JsonResponse({'success': False, 'error': 'No student name provided'}, status=400)

        # Get the class, making sure it belongs to this professor
        class_obj = get_object_or_404(Class, id=class_id, professor=request.user)

        # Only allow processing during an active schedule window (Asia/Manila local time)
        now = timezone.localtime(timezone.now(), timezone.get_default_timezone())
        active_schedule = get_active_schedule(class_obj, now)
        if not active_schedule:
            return JsonResponse({
                'success': False,
                'error': 'No active class schedule at this time. QR scanning is only allowed during scheduled class hours.'
            }, status=400)

        schedule_time_str = f"{active_schedule.start_time.strftime('%H:%M')} - {active_schedule.end_time.strftime('%H:%M')}"

        # Get or create the attendance record for the current session
        attendance_record, _ = AttendanceRecord.objects.get_or_create(
            class_obj=class_obj,
            date__date=now.date(),
            schedule_time=schedule_time_str,
            defaults={
                'date': now,
            }
        )

        # Look for a matching enrolled student by full name (or username)
        enrollments = StudentClassEnrollment.objects.filter(class_obj=class_obj).select_related('student')

        matching_student = None
        lower_scanned = scanned_name.lower()
        for enrollment in enrollments:
            student = enrollment.student
            student_full_name = (student.get_full_name() or student.username).strip()
            if student_full_name.lower() == lower_scanned:
                matching_student = student
                break

        if not matching_student:
            return JsonResponse({
                'success': False,
                'error': f'No enrolled student in this class found with name "{scanned_name}"',
                'student_name': scanned_name,
            }, status=404)

        # Avoid duplicate attendance entries for this session
        if AttendanceEntry.objects.filter(
            attendance_record=attendance_record,
            student=matching_student
        ).exists():
            display_name = matching_student.get_full_name() or matching_student.username
            return JsonResponse({
                'success': False,
                'error': f'Attendance already marked for {display_name}',
                'student_name': display_name,
                'already_marked': True,
            }, status=400)

        # Create attendance entry
        AttendanceEntry.objects.create(
            attendance_record=attendance_record,
            student=matching_student
        )

        display_name = matching_student.get_full_name() or matching_student.username
        return JsonResponse({
            'success': True,
            'message': f'Attendance marked for {display_name}',
            'student_name': display_name,
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


