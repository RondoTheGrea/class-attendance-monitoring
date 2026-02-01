from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone

from professor.models import Class, StudentClassEnrollment, Announcement, AttendanceRecord
from .forms import JoinClassForm


@login_required
def dashboard(request):
    """Student dashboard showing enrolled classes"""
    # Get active tab from query parameter (defaults to 'classes')
    active_tab = request.GET.get('tab', 'classes')
    
    # Get all classes the student is enrolled in
    enrollments = StudentClassEnrollment.objects.filter(student=request.user).select_related('class_obj')
    enrolled_classes = [enrollment.class_obj for enrollment in enrollments]
    
    # Get stats for each class
    classes_with_stats = []
    for class_obj in enrolled_classes:
        # Get upcoming schedules
        schedules = class_obj.schedules.all()
        
        # Get recent announcements
        announcements = class_obj.announcements.all()[:3]
        
        # Get attendance records for this student
        student_attendance = AttendanceRecord.objects.filter(
            class_obj=class_obj,
            entries__student=request.user
        ).distinct().count()
        
        classes_with_stats.append({
            'class_obj': class_obj,
            'schedules': schedules,
            'announcements': announcements,
            'attendance_count': student_attendance,
        })
    
    context = {
        'classes': classes_with_stats,
        'active_tab': active_tab,
    }
    return render(request, 'student/dashboard.html', context)


@login_required
def join_class(request):
    """Allow students to join a class using a class code"""
    if request.method == 'POST':
        form = JoinClassForm(request.POST)
        if form.is_valid():
            class_code = form.cleaned_data['class_code']
            try:
                class_obj = Class.objects.get(class_code=class_code)
                
                # Check if student is already enrolled
                if StudentClassEnrollment.objects.filter(student=request.user, class_obj=class_obj).exists():
                    messages.warning(request, f'You are already enrolled in "{class_obj.subject}"')
                    return redirect('student:dashboard')
                
                # Enroll the student
                StudentClassEnrollment.objects.create(
                    student=request.user,
                    class_obj=class_obj
                )
                messages.success(request, f'Successfully joined "{class_obj.subject}"!')
                return redirect('student:class_detail', class_id=class_obj.id)
            except Class.DoesNotExist:
                messages.error(request, 'Invalid class code. Please check and try again.')
    else:
        form = JoinClassForm()
    
    return render(request, 'student/join_class.html', {'form': form})


@login_required
def class_detail(request, class_id):
    """Student view of a class detail"""
    # Check if student is enrolled
    enrollment = get_object_or_404(
        StudentClassEnrollment,
        student=request.user,
        class_obj_id=class_id
    )
    class_obj = enrollment.class_obj
    
    # Get active tab from query parameter
    active_tab = request.GET.get('tab', 'overview')
    
    # Get schedules
    schedules = class_obj.schedules.all()
    
    # Get announcements
    announcements = class_obj.announcements.all()
    
    # Get attendance records for this student
    attendance_records = AttendanceRecord.objects.filter(
        class_obj=class_obj,
        entries__student=request.user
    ).distinct().order_by('-date')
    
    # Get total attendance count
    total_attendance = attendance_records.count()
    
    # Get total possible sessions (sessions that have been held)
    total_sessions = AttendanceRecord.objects.filter(class_obj=class_obj).count()
    
    context = {
        'class_obj': class_obj,
        'schedules': schedules,
        'announcements': announcements,
        'attendance_records': attendance_records,
        'active_tab': active_tab,
        'total_attendance': total_attendance,
        'total_sessions': total_sessions,
    }
    
    return render(request, 'student/class_detail.html', context)


@login_required
def leave_class(request, class_id):
    """Allow students to leave a class"""
    enrollment = get_object_or_404(
        StudentClassEnrollment,
        student=request.user,
        class_obj_id=class_id
    )
    class_name = enrollment.class_obj.subject
    enrollment.delete()
    messages.success(request, f'You have left "{class_name}"')
    return redirect('student:dashboard')


@login_required
def my_qr_code(request):
    """Display student's QR code containing their full name"""
    student_name = request.user.get_full_name() or request.user.username
    
    context = {
        'student_name': student_name,
        'qr_data': student_name,  # QR code contains the student's name
    }
    
    return render(request, 'student/my_qr_code.html', context)
