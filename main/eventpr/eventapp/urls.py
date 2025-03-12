from django.urls import path
from . import views
app_name = "eventapp"


urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('events/', views.event_list, name='events'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),  # Fixed placement
    path('booking/<slug:slug>/', views.booking, name='booking'),
    path('select-event-type/', views.select_event_type, name="select_event_type"),
    path('customize-event/', views.customize_event, name="customize_event"),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
]

