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
from .models import EventCustomization



from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils import timezone
from datetime import date
from .models import Booking


from django.core.validators import RegexValidator, ValidationError
from django.utils import timezone
from datetime import date
from .models import Booking, EventCustomization
from django import forms
from .models import Booking, EventCustomization
from django.utils import timezone
from datetime import date
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        
        exclude = ['user', 'event', 'payment', 'total_amount']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cus_name': forms.TextInput(attrs={'placeholder': 'Enter your name', 'class': 'form-control'}),
            'cus_email': forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control'}),
            'cus_ph': forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'class': 'form-control'}),
            'venue': forms.TextInput(attrs={'placeholder': 'Preferred Event Venue', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Event details', 'class': 'form-control'}),
            'customer_request': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Special requests or changes', 'class': 'form-control'}),
        }
        labels = {
            'cus_name': 'Full Name',
            'cus_email': 'Email',
            'cus_ph': 'Phone',
            'booking_date': 'Preferred Booking Date',
            'venue': 'Venue',
            'description': 'Event Details',
            'customer_request': 'Special Requests'
        }

    def __init__(self, *args, **kwargs):
        event_instance = kwargs.pop('event_instance', None)
        super().__init__(*args, **kwargs)

        if event_instance:
            self.fields['venue'].initial = event_instance.location if event_instance.location else "Custom Venue"
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
        cus_ph = self.cleaned_data.get('cus_ph').strip()
        if not cus_ph.isdigit() or len(cus_ph) != 10:
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        return cus_ph

import json
from django import forms
from .models import EventCustomization
from .models import AddOn  # For dynamic choice population

import json
from django import forms
from .models import EventCustomization, AddOn

import json
from django import forms
from .models import EventCustomization, AddOn
import json
from django import forms
from .models import EventCustomization, AddOn

import json
from django import forms
from .models import EventCustomization, AddOn

from django import forms
import json
from .models import EventCustomization, AddOn

from django import forms
import json
from .models import EventCustomization, AddOn

class EventCustomizationForm(forms.ModelForm):
    class Meta:
        model = EventCustomization
        fields = [
            'tier', 'guest_count', 'venue_size', 'catering', 'decorations',
            'entertainment', 'seating_arrangement', 'photography', 'lighting_effects',
            'table_arrangements', 'audio_visual', 'medical_support', 'event_manager',
            'cleanup_service', 'selected_location',
        ]
        widgets = {
            'tier': forms.HiddenInput(),  # Use hidden widget for tier
            'guest_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 200}),
            'venue_size': forms.Select(attrs={'class': 'form-select'}),
            'catering': forms.Select(attrs={'class': 'form-select'}),
            'decorations': forms.Select(attrs={'class': 'form-select'}),
            'entertainment': forms.Select(attrs={'class': 'form-select'}),
            'seating_arrangement': forms.Select(attrs={'class': 'form-select'}),
            'photography': forms.Select(attrs={'class': 'form-select'}),
            'lighting_effects': forms.Select(attrs={'class': 'form-select'}),
            'table_arrangements': forms.Select(attrs={'class': 'form-select'}),
            'audio_visual': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'medical_support': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'event_manager': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cleanup_service': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'selected_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your custom venue location or select from map'
            }),
        }

    def __init__(self, *args, **kwargs):
        selected_tier = kwargs.pop('selected_tier', 'Minimal')
        super().__init__(*args, **kwargs)

        # Set default initial value for tier if instance is not provided.
        if not self.instance.pk:
            self.initial.setdefault('tier', selected_tier)
            self.initial.setdefault('catering', 'None')
            self.initial.setdefault('decorations', 'None')
            self.initial.setdefault('entertainment', 'None')
            self.initial.setdefault('seating_arrangement', 'None')
            self.initial.setdefault('photography', 'None')
            self.initial.setdefault('lighting_effects', 'None')
            self.initial.setdefault('table_arrangements', 'None')

        # Explicitly mark addon fields as not required.
        for field in ['catering', 'decorations', 'entertainment', 'seating_arrangement',
                      'photography', 'lighting_effects', 'table_arrangements']:
            self.fields[field].required = False

        for field in ['audio_visual', 'medical_support', 'event_manager', 'cleanup_service']:
            self.fields[field].required = False

        # Pre-load all AddOn objects into a cache to optimize DB queries.
        dynamic_fields = ['catering', 'decorations', 'entertainment', 'photography', 'lighting_effects', 'table_arrangements']
        addon_cache = {addon.name: addon for addon in AddOn.objects.filter(name__in=dynamic_fields)}

        for field in dynamic_fields:
            try:
                addon = addon_cache.get(field)
                if addon:
                    options_dict = addon.options if isinstance(addon.options, dict) else json.loads(addon.options)
                    choices = [
                        (option, option)
                        for option, prices in options_dict.items()
                        if selected_tier in prices and prices[selected_tier] is not None
                    ]
                    self.fields[field].choices = [('None', 'None')] + choices
                else:
                    self.fields[field].choices = [('None', 'Not Available')]
            except Exception as e:
                self.fields[field].choices = [('None', 'Error Loading Options')]

    def clean_guest_count(self):
        guest_count = self.cleaned_data.get('guest_count')
        tier = self.cleaned_data.get('tier')
        max_guests = {"Minimal": 50, "Medium": 100, "Premium": 200}
        if tier and guest_count > max_guests.get(tier, 50):
            raise forms.ValidationError(f"Max guests allowed for {tier} tier is {max_guests[tier]}.")
        return guest_count

    def clean(self):
        cleaned_data = super().clean()
        tier = cleaned_data.get("tier")
        if not tier:
            return cleaned_data

        restrictions = {
            "Minimal": {
                "decorations": ["Basic", "None"],
                "entertainment": ["None"],
                "photography": ["None"]
            },
            "Medium": {
                "decorations": ["Basic", "Themed", "None"],
                "entertainment": ["None", "DJ"],
                "photography": ["None", "Basic"]
            },
            "Premium": {
                "decorations": ["Basic", "Themed", "Luxury", "None"],
                "entertainment": ["None", "DJ", "Live Band", "Projector"],
                "photography": ["None", "Basic", "Professional"]
            },
        }

        tier_restrictions = restrictions.get(tier)
        if tier_restrictions:
            for field, allowed_values in tier_restrictions.items():
                field_value = cleaned_data.get(field)
                if field_value and field_value not in allowed_values:
                    self.add_error(field, f"The selected {field} option '{field_value}' is not allowed for the {tier} tier. Allowed options: {', '.join(allowed_values)}.")
        return cleaned_data


class EventTypeForm(forms.Form):
    EVENT_TYPES = [
        ('wedding', 'Wedding'),
        ('birthday', 'Birthday'),
        ('corporate', 'Corporate'),
        ('concert', 'Concert'),
        ('exhibition', 'Exhibition'),
    ]
    event_type = forms.ChoiceField(choices=EVENT_TYPES, widget=forms.Select(attrs={'class': 'form-select'}))


from django import forms
from userapp.models import ChangeRequest

class ChangeRequestForm(forms.ModelForm):
    customer_request = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Please describe your change request...', 'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = ChangeRequest
        fields = ['request_type', 'new_value', 'customer_request']
        widgets = {
            'request_type': forms.Select(attrs={'class': 'form-control'}),
            'new_value': forms.TextInput(attrs={'class': 'form-control'}),
        }



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

class DateInput(forms.DateInput):
    input_type = 'date'

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

        