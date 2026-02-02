from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Q
from datetime import datetime, timedelta
import json

from django.contrib.auth.models import User
from .models import Class, Schedule, Announcement, AttendanceRecord, AttendanceEntry, StudentClassEnrollment, ExtraClass
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
    
    # Get all schedules for the calendar view
    all_schedules = Schedule.objects.filter(class_obj__professor=request.user).select_related('class_obj')
    
    # Build a dictionary of day -> list of schedules for JavaScript
    schedules_by_day = {}
    for schedule in all_schedules:
        day = schedule.day
        if day not in schedules_by_day:
            schedules_by_day[day] = []
        schedules_by_day[day].append({
            'id': schedule.id,
            'class_id': schedule.class_obj.id,
            'class_name': schedule.class_obj.subject,
            'start_time': schedule.start_time.strftime('%H:%M'),
            'end_time': schedule.end_time.strftime('%H:%M'),
        })
    
    # Get all extra classes for the calendar
    all_extra_classes = ExtraClass.objects.filter(class_obj__professor=request.user).select_related('class_obj')
    
    # Build a dictionary of date -> list of extra classes
    extra_classes_by_date = {}
    for extra in all_extra_classes:
        date_str = extra.date.strftime('%Y-%m-%d')
        if date_str not in extra_classes_by_date:
            extra_classes_by_date[date_str] = []
        extra_classes_by_date[date_str].append({
            'id': extra.id,
            'class_id': extra.class_obj.id,
            'class_name': extra.class_obj.subject,
            'start_time': extra.start_time.strftime('%H:%M'),
            'end_time': extra.end_time.strftime('%H:%M'),
            'reason': extra.reason or '',
        })
    
    # Get all canceled classes for the calendar
    canceled_records = AttendanceRecord.objects.filter(
        class_obj__professor=request.user,
        canceled=True
    ).select_related('class_obj')
    
    # Build a dictionary of date -> list of canceled schedule times
    canceled_classes = {}
    for record in canceled_records:
        # Use date() to ensure we get just the date part, avoiding timezone issues
        date_str = record.date.date().strftime('%Y-%m-%d')
        if date_str not in canceled_classes:
            canceled_classes[date_str] = []
        canceled_classes[date_str].append({
            'class_id': record.class_obj.id,
            'class_name': record.class_obj.subject,
            'schedule_time': record.schedule_time,
        })

    context = {
        'classes': classes,
        'active_tab': active_tab,
        'schedules_by_day': json.dumps(schedules_by_day),
        'extra_classes_by_date': json.dumps(extra_classes_by_date),
        'canceled_classes': json.dumps(canceled_classes),
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
    
    # Get extra classes (one-time sessions)
    extra_classes = class_obj.extra_classes.all()
    
    # Get announcements
    announcements = class_obj.announcements.all()
    
    # Get attendance records
    attendance_records = class_obj.attendance_records.all()
    
    # Get enrolled students
    enrolled_students = class_obj.enrolled_students.select_related('student').all()
    
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
    
    # Get today's date for extra class badges
    from datetime import date
    today = date.today()
    
    context = {
        'class_obj': class_obj,
        'schedules': schedules,
        'extra_classes': extra_classes,
        'announcements': announcements,
        'attendance_records': attendance_records,
        'enrolled_students': enrolled_students,
        'active_tab': active_tab,
        'total_students': total_students,
        'total_sessions': total_sessions,
        'attendance_rate': attendance_rate,
        'today': today,
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


def format_time_12h(t):
    """Helper to format time in 12-hour format"""
    hour = t.hour
    minute = t.minute
    ampm = 'PM' if hour >= 12 else 'AM'
    hour12 = hour % 12 or 12
    return f"{hour12}:{minute:02d} {ampm}"


def check_time_overlap(start1, end1, start2, end2):
    """Check if two time ranges overlap. Times should be in minutes from midnight."""
    return (start1 < end2) and (end1 > start2)


def time_to_minutes(t):
    """Convert time object to minutes from midnight"""
    return t.hour * 60 + t.minute


@login_required
def add_schedule(request, class_id):
    """Add a schedule to a class"""
    class_obj = get_object_or_404(Class, id=class_id, professor=request.user)
    
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.class_obj = class_obj
            
            # Validate times
            if schedule.start_time >= schedule.end_time:
                messages.error(request, '⚠️ Invalid time range: Start time must be before end time.')
                return redirect('professor:class_detail', class_id=class_id)
            
            new_start = time_to_minutes(schedule.start_time)
            new_end = time_to_minutes(schedule.end_time)
            
            # Check for conflicts with existing weekly schedules on same day
            existing_schedules = Schedule.objects.filter(
                class_obj=class_obj,
                day=schedule.day
            )
            
            for existing in existing_schedules:
                existing_start = time_to_minutes(existing.start_time)
                existing_end = time_to_minutes(existing.end_time)
                
                if check_time_overlap(new_start, new_end, existing_start, existing_end):
                    conflict_time = f"{format_time_12h(existing.start_time)} - {format_time_12h(existing.end_time)}"
                    messages.error(
                        request, 
                        f'⚠️ Schedule Conflict: This time overlaps with an existing {schedule.day} schedule ({conflict_time}). Please choose a different time.'
                    )
                    return redirect('professor:class_detail', class_id=class_id)
            
            schedule.save()
            messages.success(request, '✅ Weekly schedule added successfully!')
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
def add_extra_class(request, class_id):
    """Add an extra/one-time class session"""
    class_obj = get_object_or_404(Class, id=class_id, professor=request.user)
    
    if request.method == 'POST':
        date_str = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        reason = request.POST.get('reason', '')
        
        if date_str and start_time and end_time:
            from datetime import datetime
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                start_time_obj = datetime.strptime(start_time, '%H:%M').time()
                end_time_obj = datetime.strptime(end_time, '%H:%M').time()
                
                # Validate times
                if start_time_obj >= end_time_obj:
                    messages.error(request, '⚠️ Invalid time range: Start time must be before end time.')
                    return redirect('professor:class_detail', class_id=class_id)
                
                new_start = time_to_minutes(start_time_obj)
                new_end = time_to_minutes(end_time_obj)
                
                # Get day of week for the selected date
                day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                day_of_week = day_names[date_obj.weekday()]
                
                # Check for conflicts with weekly schedules on this day of week
                weekly_schedules = Schedule.objects.filter(
                    class_obj=class_obj,
                    day=day_of_week
                )
                
                for schedule in weekly_schedules:
                    sched_start = time_to_minutes(schedule.start_time)
                    sched_end = time_to_minutes(schedule.end_time)
                    
                    if check_time_overlap(new_start, new_end, sched_start, sched_end):
                        conflict_time = f"{format_time_12h(schedule.start_time)} - {format_time_12h(schedule.end_time)}"
                        messages.error(
                            request, 
                            f'⚠️ Schedule Conflict: This time overlaps with a regular {day_of_week} class ({conflict_time}). Please choose a different time.'
                        )
                        return redirect('professor:class_detail', class_id=class_id)
                
                # Check for conflicts with other extra classes on the same date
                existing_extras = ExtraClass.objects.filter(
                    class_obj=class_obj,
                    date=date_obj
                )
                
                for extra in existing_extras:
                    extra_start = time_to_minutes(extra.start_time)
                    extra_end = time_to_minutes(extra.end_time)
                    
                    if check_time_overlap(new_start, new_end, extra_start, extra_end):
                        conflict_time = f"{format_time_12h(extra.start_time)} - {format_time_12h(extra.end_time)}"
                        messages.error(
                            request, 
                            f'⚠️ Schedule Conflict: This time overlaps with another extra class on {date_obj.strftime("%B %d, %Y")} ({conflict_time}). Please choose a different time.'
                        )
                        return redirect('professor:class_detail', class_id=class_id)
                
                # No conflicts, create the extra class
                extra = ExtraClass.objects.create(
                    class_obj=class_obj,
                    date=date_obj,
                    start_time=start_time_obj,
                    end_time=end_time_obj,
                    reason=reason
                )
                
                # Create announcement for this extra class
                formatted_date = date_obj.strftime('%B %d, %Y')
                time_range = f"{format_time_12h(start_time_obj)} - {format_time_12h(end_time_obj)}"
                announcement_title = f"Extra Class: {formatted_date} ({time_range})"
                announcement_content = reason if reason else "An extra class session has been scheduled."
                
                Announcement.objects.create(
                    class_obj=class_obj,
                    title=announcement_title,
                    content=announcement_content
                )
                
                messages.success(request, '✅ Extra class added and announcement created!')
            except ValueError as e:
                messages.error(request, f'⚠️ Invalid date or time format: {e}')
        else:
            messages.error(request, '⚠️ Please fill in all required fields.')
    
    return redirect('professor:class_detail', class_id=class_id)


@login_required
def delete_extra_class(request, class_id, extra_class_id):
    """Delete an extra class"""
    class_obj = get_object_or_404(Class, id=class_id, professor=request.user)
    extra_class = get_object_or_404(ExtraClass, id=extra_class_id, class_obj=class_obj)
    extra_class.delete()
    messages.success(request, 'Extra class deleted successfully!')
    return redirect('professor:class_detail', class_id=class_id)


@login_required
def kick_student(request, class_id, enrollment_id):
    """Remove a student from a class"""
    class_obj = get_object_or_404(Class, id=class_id, professor=request.user)
    enrollment = get_object_or_404(StudentClassEnrollment, id=enrollment_id, class_obj=class_obj)
    
    if request.method == 'POST':
        student_name = enrollment.student.get_full_name() or enrollment.student.username
        enrollment.delete()
        messages.success(request, f'{student_name} has been removed from the class.')
    
    return redirect('professor:class_detail', class_id=class_id)


@login_required
def cancel_class(request):
    """Cancel a class for a specific date"""
    if request.method == 'POST':
        schedule_id = request.POST.get('schedule_id')
        cancel_date = request.POST.get('cancel_date')  # Format: YYYY-MM-DD
        
        schedule = get_object_or_404(Schedule, id=schedule_id, class_obj__professor=request.user)
        
        # Parse the date - use noon to avoid timezone date boundary issues
        from datetime import datetime
        date_obj = datetime.strptime(cancel_date, '%Y-%m-%d')
        date_obj = date_obj.replace(hour=12, minute=0, second=0)
        
        schedule_time_str = f"{schedule.start_time.strftime('%H:%M')} - {schedule.end_time.strftime('%H:%M')}"
        
        # Get announcement data (only for canceling, not uncanceling)
        announcement_title = request.POST.get('announcement_title', '')
        announcement_content = request.POST.get('announcement_content', '')
        
        # Check if there's already an attendance record for this schedule on this date
        existing = AttendanceRecord.objects.filter(
            class_obj=schedule.class_obj,
            date__date=date_obj.date(),
            schedule_time=schedule_time_str
        ).first()
        
        if existing:
            # Toggle the canceled status
            existing.canceled = not existing.canceled
            existing.save()
            if existing.canceled:
                # Create announcement when canceling
                if announcement_title and announcement_content:
                    Announcement.objects.create(
                        class_obj=schedule.class_obj,
                        title=announcement_title,
                        content=announcement_content
                    )
                messages.success(request, f'Class "{schedule.class_obj.subject}" has been canceled for {cancel_date}.')
            else:
                # Create announcement when uncanceling
                if announcement_title and announcement_content:
                    Announcement.objects.create(
                        class_obj=schedule.class_obj,
                        title=announcement_title,
                        content=announcement_content
                    )
                messages.success(request, f'Class "{schedule.class_obj.subject}" has been restored for {cancel_date}.')
        else:
            # Create a new attendance record marked as canceled
            AttendanceRecord.objects.create(
                class_obj=schedule.class_obj,
                date=date_obj,
                schedule_time=schedule_time_str,
                canceled=True
            )
            # Create announcement when canceling
            if announcement_title and announcement_content:
                Announcement.objects.create(
                    class_obj=schedule.class_obj,
                    title=announcement_title,
                    content=announcement_content
                )
            messages.success(request, f'Class "{schedule.class_obj.subject}" has been canceled for {cancel_date}.')
    
    from django.urls import reverse
    return redirect(reverse('professor:dashboard') + '?tab=schedules')


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


