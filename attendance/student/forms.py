from django import forms


class JoinClassForm(forms.Form):
    """Form for students to join a class using a class code"""
    class_code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter 6-digit class code',
            'style': 'text-transform: uppercase; letter-spacing: 0.2em; font-size: 18px; text-align: center;',
            'maxlength': '6',
            'pattern': '[A-Z0-9]{6}',
        }),
        help_text='Enter the 6-digit code provided by your professor'
    )

    def clean_class_code(self):
        code = self.cleaned_data.get('class_code', '').upper().strip()
        if len(code) != 6:
            raise forms.ValidationError("Class code must be exactly 6 characters.")
        return code
