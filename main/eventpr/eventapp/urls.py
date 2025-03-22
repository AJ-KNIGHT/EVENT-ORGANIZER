from django.urls import path
from . import views

app_name = "eventapp"

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('events/', views.event_list, name='events'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    path('booking/<slug:slug>/', views.booking, name='booking'),
    path('select-event-type/<slug:slug>/', views.select_event_type, name="select_event_type"),
    path("customize_event/", views.customize_event, name="customize_event"),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('chatbot-response/', views.chatbot_response, name='chatbot_response'),
    path('update_price/', views.update_price, name='update_price'),
    path('event-location/', views.event_location, name='event_location'),
    path('select-event-date/', views.select_event_date, name='select_event_date'),
    path('select_venue_tier/', views.select_venue_tier, name='select_venue_tier'),
    path('customization-summary/<int:booking_id>/', views.customization_summary, name='customization_summary'),
    path('addon-details/<str:addon_name>/', views.addon_details, name='addon_details'),
]
