from django.contrib import admin
from .models import Event, Booking, Contact 

# Register the Event and Contact models
admin.site.register(Event)
admin.site.register(Contact)

# Register the Booking model with custom admin
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'cus_name', 'event_name', 'event_date', 'venue', 'booking_date')

# Only register Booking with the BookingAdmin class
admin.site.register(Booking, BookingAdmin)
