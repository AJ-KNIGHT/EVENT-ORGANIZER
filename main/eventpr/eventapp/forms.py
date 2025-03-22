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

from django import forms
from .models import Booking, EventCustomization, AddOn
from django.core.validators import RegexValidator, validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date
import json

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, RegexValidator
from django.utils import timezone
from datetime import date
import json
from .models import Booking, EventCustomization, AddOn
from userapp.models import ChangeRequest


# legacy but still helps in backend logic , but isnt shown to user
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
            self.fields['booking_date'].widget.attrs['min'] = timezone.localdate()

    def clean_booking_date(self):
        booking_date = self.cleaned_data.get('booking_date')
        if booking_date < timezone.localdate():
            raise forms.ValidationError("Booking date cannot be in the past.")
        return booking_date

class EventCustomizationForm(forms.ModelForm):
    class Meta:
        model = EventCustomization
        fields = ['tier', 'guest_count', 'venue_size', 'selected_location', 'venue_subtier', 'custom_venue_description']
        widgets = {
            'tier': forms.HiddenInput(),
            'guest_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 200}),
            'venue_size': forms.Select(attrs={'class': 'form-select'}),
            'selected_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your custom venue location or select from map'
            }),
            'venue_subtier': forms.HiddenInput(),
            'custom_venue_description': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        selected_tier = kwargs.pop('selected_tier', 'Minimal')
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            self.initial.setdefault('tier', selected_tier)

        # Dynamically generate form fields based on add-ons
        if self.instance and self.instance.add_ons:
            add_ons = self.instance.add_ons
            for field, value in add_ons.items():
                if isinstance(value, list):  # Choices for the add-on
                    self.fields[field] = forms.ChoiceField(
                        choices=[(opt, opt) for opt in value],
                        required=False,
                        widget=forms.Select(attrs={'class': 'form-select'})
                    )
                elif isinstance(value, bool):  # Boolean (checkbox)
                    self.fields[field] = forms.BooleanField(
                        required=False,
                        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
                    )

        # Set required to False for dynamic fields (they are optional)
        for field in self.fields:
            if isinstance(self.fields[field], (forms.BooleanField, forms.ChoiceField)):
                self.fields[field].required = False

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

        # Tier-based restrictions (dynamically set as per the tier)
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
        
        venue_subtier = cleaned_data.get("venue_subtier")
        if venue_subtier not in ["Minimal", "Medium", "Luxury", "Custom"]:
            self.add_error("venue_subtier", f"Invalid venue subtier '{venue_subtier}'. Allowed values: Minimal, Medium, Luxury, Custom.")
        
        return cleaned_data



# ------------------------------
# EventTypeForm – for selecting event type at the beginning
# ------------------------------
class EventTypeForm(forms.Form):
    EVENT_TYPES = [
        ('wedding', 'Wedding'),
        ('birthday', 'Birthday'),
        ('corporate', 'Corporate'),
        ('concert', 'Concert'),
        ('exhibition', 'Exhibition'),
    ]
    event_type = forms.ChoiceField(choices=EVENT_TYPES, widget=forms.Select(attrs={'class': 'form-select'}))


# ------------------------------
# ChangeRequestForm – updated for more detailed change requests
# ------------------------------
class ChangeRequestForm(forms.ModelForm):
    additional_details = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Provide additional details if necessary...', 'class': 'form-control'}),
        required=False,
        label="Additional Details"
    )

    class Meta:
        model = ChangeRequest
        fields = ['request_type', 'new_value', 'customer_request', 'additional_details']
        widgets = {
            'request_type': forms.Select(attrs={'class': 'form-control'}),
            'new_value': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_request': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['request_type'].label = "Type of Change"
        self.fields['new_value'].label = "New Value/Details"
        self.fields['customer_request'].label = "Customer Request"

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


        