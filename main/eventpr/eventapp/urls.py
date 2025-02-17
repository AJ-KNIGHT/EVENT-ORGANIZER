from django.urls import path
from . import views
app_name = "eventapp"


urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('events/', views.event_list, name='events'),
    path('booking/<slug:slug>/', views.booking, name='booking'),
    path('contact/', views.contact, name='contact'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    
]
