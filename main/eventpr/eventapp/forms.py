from django import forms
from .models import Booking , Event
from django.contrib.auth.models import User
from django.forms.widgets import DateInput 
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from datetime import datetime, date
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import datetime
from userapp.models import ChangeRequest


class DateInput(forms.DateInput):
    input_type = 'date'

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['user', 'event_name', 'event_date' , 'payment']
        fields = '__all__'
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cus_name': forms.TextInput(attrs={'placeholder': 'Enter your name', 'class': 'form-control'}),
            'cus_email': forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control'}),
            'cus_ph': forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'class': 'form-control'}),
            'venue': forms.TextInput(attrs={'placeholder': 'Preferred Event Venue', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter event description', 'class': 'form-control'}),
            'customer_request': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter any special requests or changes', 'class': 'form-control'}),
        }
        labels = {
            'cus_name': 'Enter Your Full Name',
            'cus_email': 'Enter Your Email',
            'cus_ph': 'Enter Your Phone',
            'booking_date': 'Preferred Booking Date',
            'venue': 'Preferred Venue',
            'description': 'Event Description',
            'customer_request': 'Special Requests/Changes'
        }

    def __init__(self, *args, **kwargs):
        event_instance = kwargs.pop('event_instance', None)
        super().__init__(*args, **kwargs)

        if event_instance:
            self.fields['venue'].initial = event_instance.location
            self.fields['booking_date'].initial = timezone.localdate()

    def clean_booking_date(self):
        booking_date = self.cleaned_data.get('booking_date')
        if booking_date < date.today():
            raise forms.ValidationError("Booking date cannot be in the past.")
        return booking_date

    def clean_cus_email(self):
        email = self.cleaned_data.get('cus_email')
        if not email:
            raise forms.ValidationError("Email is required.")
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Enter a valid email address.")
        return email

    def clean_cus_ph(self):
        cus_ph = self.cleaned_data.get('cus_ph')
        cus_ph = cus_ph.strip()
        if not cus_ph.isdigit() or len(cus_ph) != 10:
            raise forms.ValidationError("Please enter a valid 10-digit phone number.")
        return cus_ph





class ChangeRequestForm(forms.Form):
    customer_request = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Please describe your change request...'}))


# New SignupForm for user registration
from django import forms
from userapp.models import CustomUser  # Import your CustomUser model

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), label='Confirm Password')

    class Meta:
        model = CustomUser  # Use CustomUser instead of User
        fields = ['username', 'email', 'phone_number', 'password']  # Add phone_number

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            user.save()
        return user


from django import forms
from userapp.models import ChangeRequest

class ChangeRequestForm(forms.ModelForm):
    class Meta:
        model = ChangeRequest
        fields = ['request_type', 'new_value']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set field labels
        self.fields['request_type'].label = "Type of Change"
        self.fields['new_value'].label = "New Value/Details"
        
        # Add CSS classes to form fields
        self.fields['request_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['new_value'].widget.attrs.update({'class': 'form-control'})

        