from django import template
from datetime import time, timedelta

register = template.Library()


@register.filter
def format_time(value):
    """Format a time object to 12-hour format with AM/PM"""
    if isinstance(value, time):
        hour = value.hour
        minute = value.minute
        am_pm = "AM" if hour < 12 else "PM"
        display_hour = hour if hour <= 12 else hour - 12
        if display_hour == 0:
            display_hour = 12
        return f"{display_hour}:{minute:02d} {am_pm}"
    return value


@register.filter
def time_duration(start_time, end_time):
    """Calculate duration between two times as percentage of day"""
    if isinstance(start_time, time) and isinstance(end_time, time):
        start_minutes = start_time.hour * 60 + start_time.minute
        end_minutes = end_time.hour * 60 + end_time.minute
        duration_minutes = end_minutes - start_minutes
        # Convert to percentage of 24 hours (1440 minutes)
        return (duration_minutes / 1440) * 100
    return 0
