from django.contrib import admin
from .models import Event
from .models import Booking
from .models import Contact

# Register your models here.
admin.site.register(Event)
admin.site.register(Booking)
admin.site.register(Contact)