from django import template
from datetime import time

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
