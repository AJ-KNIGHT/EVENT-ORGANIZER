from django.contrib import admin
from .models import Event, Booking, Contact 

# Register the Event and Contact models
admin.site.register(Event)
admin.site.register(Contact)

# Register the Booking model with custom admin
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_event_name', 'booking_date', 'venue')

    def get_event_name(self, obj):
        return obj.event.name  # Assuming Event model has 'name' field

    get_event_name.admin_order_field = 'event'  # Allows sorting by event name
    get_event_name.short_description = 'Event Name'  # Column header in Admin panel


# Only register Booking with the BookingAdmin class
admin.site.register(Booking, BookingAdmin)
