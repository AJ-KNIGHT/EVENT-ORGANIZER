from django import forms
from .models import Booking

class DateInput(forms.DateInput):
    input_type = 'date'

# forms.py
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['cus_name', 'cus_ph', 'event_name', 'event_date', 'venue', 'description']
        widgets = {
            'event_date': DateInput(),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter event description'}),
        }
        labels = {
            'cus_name': 'Customer Name:',
            'cus_ph': 'Customer Phone:',
            'event_name': 'Event Name:',
            'event_date': 'Event Date:',
            'venue': 'Venue:',
            'description': 'Event Description:',
        }

    # forms.py
def clean_cus_ph(self):
    cus_ph = self.cleaned_data.get('cus_ph')
    if not cus_ph.isdigit() or len(cus_ph) != 10:
        raise forms.ValidationError("Please enter a valid 10-digit phone number (without any spaces or special characters).")
    return cus_ph
