""" from django.shortcuts import render,redirect,get_object_or_404
from .models import Event
from .models import Booking
from .forms import BookingForm
from django.contrib import messages
from .models import Contact
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    return render(request,'index.html')
def about(request):
    return render(request,'about.html')

def event_list(request):
    events = Event.objects.all().order_by('event_date')  # Order by event date
    paginator = Paginator(events, 6)  # Show 6 events per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'eventapp/events.html', {'page_obj': page_obj})

def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    # Fetch related events (excluding the current one)
    related_events = Event.objects.filter(event_type=event.event_type).exclude(id=event.id)[:3]
    return render(request, 'eventapp/event_detail.html', {'event': event, 'related_events': related_events})


# views.py
def booking(request, id=None):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.event_name = event.name  # Link to the specific event
            booking.venue = event.location
            booking.event_date = event.event_date
            booking.save()
            messages.success(request, "Your event has been booked successfully!")
            return redirect('events')
    else:
        form = BookingForm()
    return render(request, 'eventapp/booking.html', {'form': form, 'event': event})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Save the contact submission to the database
        Contact.objects.create(name=name, email=email, message=message)

        # Display a success message
        messages.success(request, 'Thank you for reaching out! We will get back to you soon.')
        return redirect('contact')  # Redirect to the contact page

    return render(request, 'contact.html')
 """

from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Booking
from .forms import BookingForm
from django.contrib import messages
from .models import Contact
from django.core.paginator import Paginator

# Home Page
def index(request):
    events = Event.objects.all().order_by('event_date')[:3]  # Get featured events (limit to 3 for home page)
    return render(request, 'index.html', {'events': events})


# About Page
def about(request):
    return render(request, 'about.html')

# Event List View
def event_list(request):
    events = Event.objects.all().order_by('event_date')  # or however you're fetching the events
    paginator = Paginator(events, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'page_obj': page_obj})


# Event Detail View using Slug
def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    related_events = Event.objects.filter(event_type=event.event_type).exclude(id=event.id)[:3]
    return render(request, 'event_details.html', {'event': event, 'related_events': related_events})


# Booking View
def booking(request, slug=None):
    event = get_object_or_404(Event, slug=slug)  # Fetch event by slug
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.event_name = event.name
            booking.venue = event.location
            booking.event_date = event.event_date
            booking.save()
            messages.success(request, "Your event has been booked successfully!")
            return redirect('events')
    else:
        form = BookingForm()
    return render(request, 'templates/booking.html', {'form': form, 'event': event})


# Contact Form Handling
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        Contact.objects.create(name=name, email=email, message=message)
        messages.success(request, 'Thank you for reaching out! We will get back to you soon.')
        return redirect('contact')  # Redirect to the contact page
    return render(request, 'contact.html')
