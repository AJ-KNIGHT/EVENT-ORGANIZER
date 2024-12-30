from django import forms
from .models import Booking
from django.contrib.auth.models import User
from django.forms.widgets import DateInput 
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from datetime import datetime, date


class DateInput(forms.DateInput):
    input_type = 'date'
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['cus_name', 'cus_email', 'cus_ph', 'event_name', 'booking_date', 'venue', 'description', 'customer_request']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),  # Custom booking date
            'cus_name': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'cus_email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'cus_ph': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
            'event_name': forms.TextInput(attrs={'readonly': 'readonly', 'placeholder': 'Event Name'}),
            'venue': forms.TextInput(attrs={'placeholder': 'Preferred Event Venue'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter event description'}),
            'customer_request': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter any special requests or changes'}),
            'event_date': forms.DateInput(attrs={'readonly': 'readonly', 'type': 'date'}),  # Read-only event date
        }
        labels = {
            'cus_name': 'Customer Name:',
            'cus_email': 'Customer Email:',
            'cus_ph': 'Customer Phone:',
            'event_name': 'Event Name:',
            'event_date': 'Event Availability Date:',
            'booking_date': 'Preferred Booking Date:',
            'venue': 'Preferred Venue:',
            'description': 'Event Description:',
            'customer_request': 'Special Requests/Changes:'
        }

    def __init__(self, *args, **kwargs):
        event_instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        
        if event_instance:
            # Pre-populate event_date with event's availability date if an event instance exists
            self.fields['event_date'].initial = event_instance.event_date
            self.instance.event_date = event_instance.event_date  # Ensure it's set in the model instance

    def clean_booking_date(self):
        booking_date = self.cleaned_data.get('booking_date')
        event_date = self.cleaned_data.get('event_date')
        
        if isinstance(booking_date, datetime):
            booking_date = booking_date.date()

        if booking_date < date.today():
            raise forms.ValidationError("The booking date cannot be in the past.")
        
        # Ensure event_date is not empty or None, set it to the event's date if missing
        if not event_date:
            event_date = self.instance.event_date  # Fallback to event's date if not provided
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
        cus_ph = cus_ph.strip()  # Trim spaces
        if not cus_ph.isdigit() or len(cus_ph) != 10:
            raise forms.ValidationError("Please enter a valid 10-digit phone number (without any spaces or special characters).")
        return cus_ph



class ChangeRequestForm(forms.Form):
    customer_request = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Please describe your change request...'}))


# New SignupForm for user registration
class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data
