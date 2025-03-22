from django.contrib import admin
from .models import Event, Booking, Contact , ChatbotQA
import csv
from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from django import forms
from .models import ChatbotQA

import json
from django import forms
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import admin
from .models import ChatbotQA
from django.contrib import admin
from .models import AddOn, EventCustomization

# Register the Event and Contact models
admin.site.register(Event)
admin.site.register(Contact)


# Register the Booking model with custom admin

# Register the Booking model with custom admin
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_event_name', 'booking_date', 'venue_tier', 'total_amount', 'status')

    def get_event_name(self, obj):
        return obj.event.name  # Display the event name

    get_event_name.admin_order_field = 'event'  # Allows sorting by event name
    get_event_name.short_description = 'Event Name'  # Column header in Admin panel

    def venue_tier(self, obj):
        return obj.venue_tier  # Display the venue tier (Minimal, Medium, Luxury)

    venue_tier.short_description = 'Venue Tier'

    def total_amount(self, obj):
        return obj.total_amount  # Display the total amount for the booking

    total_amount.short_description = 'Total Amount'

admin.site.register(Booking, BookingAdmin)

#from .models import ChatbotQA

@admin.register(EventCustomization)
class EventCustomizationAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'get_event', 'get_selected_options', 'total_price')

    def get_user(self, obj):
        return obj.booking.user.username if obj.booking.user else "N/A"
    get_user.short_description = "User"

    def get_event(self, obj):
        return obj.booking.event.name if obj.booking.event else "N/A"
    get_event.short_description = "Event"

    def get_selected_options(self, obj):
        return ", ".join([f"{key}: {value['name']}" for key, value in obj.add_ons.items()])
    get_selected_options.short_description = "Selected Options"

    def total_price(self, obj):
        return obj.calculate_total_price()  # Show the calculated total price for the customization

    total_price.short_description = "Total Price"





class JsonImportForm(forms.Form):
    json_file = forms.FileField()

@admin.register(ChatbotQA)
class ChatbotQAAdmin(admin.ModelAdmin):
    list_display = ('question', 'keywords')
    search_fields = ('question', 'keywords')
    actions = ['import_csv', 'import_json']

    def import_csv(self, request):
        if request.method == "POST":
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                for row in reader:
                    ChatbotQA.objects.create(
                        question=row['question'],
                        answer=row['answer'],
                        keywords=row['keywords']
                    )
                self.message_user(request, "CSV file has been imported successfully.")
                return redirect("..")
        else:
            form = CsvImportForm()
        return render(request, "admin/csv_upload.html", {"form": form})

    def import_json(self, request):
        if request.method == "POST":
            form = JsonImportForm(request.POST, request.FILES)
            if form.is_valid():
                json_file = request.FILES['json_file']
                data = json.load(json_file)
                for item in data:
                    ChatbotQA.objects.create(
                        question=item['question'],
                        answer=item['answer'],
                        keywords=item['keywords']
                    )
                self.message_user(request, "JSON file has been imported successfully.")
                return redirect("..")
        else:
            form = JsonImportForm()
        return render(request, "admin/json_upload.html", {"form": form})

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.import_csv, name='import_csv'),
            path('import-json/', self.import_json, name='import_json'),
        ]
        return custom_urls + urls
    


@admin.register(AddOn)
class AddOnAdmin(admin.ModelAdmin):
    list_display = ('name', 'options')  # Adjust fields as needed


from django.contrib import admin
from django.utils.html import format_html
from .models import EventLocation

class EventLocationAdmin(admin.ModelAdmin):
    list_display = ("booking", "full_address", "latitude", "longitude", "maps_link")

    def maps_link(self, obj):
        """Show clickable links to open the location on different map services."""
        if obj.latitude and obj.longitude:
            return format_html(
                '<a href="{}" target="_blank" style="color: blue; font-weight: bold;">Google Maps</a> | '
                '<a href="{}" target="_blank" style="color: green; font-weight: bold;">OpenStreetMap</a>',
                obj.google_maps_link(),
                obj.openstreetmap_link(),
            )
        return "No Location Set"
    
    maps_link.short_description = "View on Map"

admin.site.register(EventLocation, EventLocationAdmin)
