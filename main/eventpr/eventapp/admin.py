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
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_event_name', 'booking_date', 'venue')

    def get_event_name(self, obj):
        return obj.event.name  # Assuming Event model has 'name' field

    get_event_name.admin_order_field = 'event'  # Allows sorting by event name
    get_event_name.short_description = 'Event Name'  # Column header in Admin panel

#from .models import ChatbotQA





# Only register Booking with the BookingAdmin class
admin.site.register(Booking, BookingAdmin)


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

@admin.register(EventCustomization)
class EventCustomizationAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'get_event', 'selected_options', 'total_price')

    def get_user(self, obj):
        return obj.booking.user.username if obj.booking.user else "N/A"
    get_user.short_description = "User"

    def get_event(self, obj):
        return obj.booking.event.name if obj.booking.event else "N/A"
    get_event.short_description = "Event"

