from django import forms
from .models import Class, Schedule, Announcement


class ClassForm(forms.ModelForm):
    """Form for creating/editing a class"""
    class Meta:
        model = Class
        fields = ['subject', 'section', 'room', 'description']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Introduction to Computer Science'
            }),
            'section': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., A, B, 101'
            }),
            'room': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Room 301'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Brief description of the class...'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].required = True
        self.fields['section'].required = False
        self.fields['room'].required = False
        self.fields['description'].required = False


class ScheduleForm(forms.ModelForm):
    """Form for adding a schedule"""
    class Meta:
        model = Schedule
        fields = ['day', 'start_time', 'end_time']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-input'
            }),
            'end_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-input'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if end_time <= start_time:
                raise forms.ValidationError("End time must be after start time.")

        return cleaned_data


class AnnouncementForm(forms.ModelForm):
    """Form for creating an announcement"""
    class Meta:
        model = Announcement
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Announcement title...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'Write your announcement here...'
            })
        }
