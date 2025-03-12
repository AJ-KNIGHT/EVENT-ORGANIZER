from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Event, Booking , Contact
from datetime import date
from .forms import BookingForm ,ChangeRequestForm 
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import datetime
#from paymentapp.models import Payment
import random
from django.contrib.auth.decorators import login_required
from eventpr.utils import send_html_email
from django.db.models import Count
from django.utils.timezone import now
from django.shortcuts import render
from .models import Event
from django.templatetags.static import static
from .forms import EventCustomizationForm , EventTypeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.templatetags.static import static
from django.conf import settings
from datetime import date

from eventapp.models import Event, Booking
from eventapp.forms import BookingForm
from paymentapp.models import Payment  # Import Payment model
from paymentapp.views import confirm_payment  # Import confirm_payment function
from userapp.utils import send_html_email  # Import email function



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from decimal import Decimal
from .models import Event, Booking, EventCustomization
from .forms import BookingForm, EventCustomizationForm, EventTypeForm
from django.templatetags.static import static


@login_required
def booking(request, slug=None):
    event = get_object_or_404(Event, slug=slug)

    if event.event_date < now().date() or not event.is_available:
        messages.error(request, "This event is no longer available for booking.")
        return redirect('event_detail', slug=slug)

    if request.method == "POST":
        booking_form = BookingForm(request.POST)
        customization_form = EventCustomizationForm(request.POST)

        if booking_form.is_valid() and customization_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.user = request.user
            booking.event = event  # ✅ Fixed mistake (event_name → event)
            booking.event_date = event.event_date
            booking.save()

            # Create or update customization
            customization, created = EventCustomization.objects.get_or_create(booking=booking)
            customization_form = EventCustomizationForm(request.POST, instance=customization)
            if customization_form.is_valid():
                customization_form.save()

            # Update total amount **before saving** (fix recursion issue)
            booking.total_amount = customization.calculate_price()
            booking.save(update_fields=['total_amount'])

            messages.success(request, "Booking successful! Your customization has been applied.")
            return redirect('booking_dashboard')

    else:
        booking_form = BookingForm()
        customization_form = EventCustomizationForm()

    return render(request, 'eventapp/booking.html', {
        'booking_form': booking_form,
        'customization_form': customization_form,
        'event': event,
    })


@login_required
def select_event_type(request):
    event_slug = request.GET.get('event')
    if event_slug:
        request.session['event_slug'] = event_slug  # Store in session

    if request.method == 'POST':
        event_type = request.POST.get('event_type')
        base_price = request.POST.get('base_price')

        if event_type:
            request.session['selected_event_type'] = event_type
            request.session['base_price'] = base_price
            return redirect('eventapp:customize_event')

    return render(request, 'eventapp/select_event_type.html')


@login_required
def customize_event(request):
    selected_event_type = request.session.get('selected_event_type')
    event_slug = request.session.get('event_slug')  # Retrieve event

    if not selected_event_type or not event_slug:
        messages.error(request, "Please select an event type first.")
        return redirect('eventapp:select_event_type')

    event = get_object_or_404(Event, slug=event_slug)  # Get event instance

    try:
        booking = Booking.objects.filter(user=request.user, event=event).latest('booking_date')  # ✅ Fixed mistake
    except Booking.DoesNotExist:
        messages.error(request, "You have no active bookings to customize.")
        return redirect('eventapp:select_event_type')

    customization, created = EventCustomization.objects.get_or_create(booking=booking)

    if request.method == 'POST':
        form = EventCustomizationForm(request.POST, instance=customization)
        if form.is_valid():
            form.save()
            booking.total_amount = customization.calculate_price()
            booking.save(update_fields=['total_amount'])
            messages.success(request, "Your event customization has been saved!")
            return redirect('paymentapp:payment_page')
    else:
        form = EventCustomizationForm(instance=customization)

    return render(request, 'eventapp/customize_event.html', {
        'form': form,
        'event': event,
        'total_price': customization.total_price
    })


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    related_events = Event.objects.filter(event_type=event.event_type).exclude(id=event.id).order_by('?')[:3]
    return render(request, 'eventapp/event_details.html', {'event': event, 'related_events': related_events})


def index(request):
    # Get all available future events
    events = Event.objects.filter(event_date__gte=now().date(), is_available=True)

    # Fetch random events
    random_events = events.order_by('?')[:3] if events.count() >= 3 else events

    # Preloaded assets for better UX
    preloaded_assets = {'video': static('images/pexel-party.mp4')}

    return render(request, 'index.html', {'events': random_events, 'preloaded_assets': preloaded_assets})


# About view
def about(request):
    preloaded_assets ={
        'about_image': static('images/pexel-about.jpg'),
    }
    return render(request, 'about.html', {'preloaded_assets': preloaded_assets})

# Event list view (for pagination)
def event_list(request):
    events = Event.objects.filter(event_date__gte=now().date(), is_available=True).order_by('event_date')  # Order by event date
    paginator = Paginator(events, 6)  # Adjust the number of events per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'eventapp/events.html', {'page_obj': page_obj})

# Contact view
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        Contact.objects.create(name=name, email=email, message=message)
        request.toast_type = 'success'  # 'error', 'warning', 'info', etc.
        request.toast_message = 'Thank you for reaching out! We will get back to you soon.'
        messages.success(request, 'Thank you for reaching out! We will get back to you soon.')
        return redirect('contact')

    # Now pass the messages_list to your template context
    preloaded_assets ={
        'contact_image': static('images/pexel-contact.jpg'),
    }
    return render(request, 'contact.html', {'preloaded_assets': preloaded_assets,})



from datetime import datetime

def base(request):
    context = {
        'current_year': datetime.now().year,
    }
    return render(request, 'base.html', context)



def privacy_policy(request):
    return render(request, 'privacy_policy.html')
def terms_of_service(request):
    return render(request, 'terms_of_service.html')