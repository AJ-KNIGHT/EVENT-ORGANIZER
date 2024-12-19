from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('events/', views.event_list, name='events'),
    path('booking/<slug:slug>/', views.booking, name='booking'),  # Use slug here
    path('contact/', views.contact, name='contact'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
]
