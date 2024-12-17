from django.shortcuts import render
from .models import Event
from .forms import BookingForm

# Create your views here.
def index(request):
    return render(request,'index.html')
def about(request):
    return render(request,'about.html')
def events(request):
    dict_eve={
        'eve':Event.objects.all
    }
    return render(request,'events.html',dict_eve)
def booking(request):
    form=BookingForm()
    dict_form={
        'form':form
    }
    return render(request,'booking.html')
def contact(request):
    return render(request,'contact.html')
