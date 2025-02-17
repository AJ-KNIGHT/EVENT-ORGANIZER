from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from eventapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),  # Keep this for the home page
    path("", include("eventapp.urls")),  # Change this to /events to avoid the conflict
    path("user/", include('userapp.urls')),
    path('payment/', include('paymentapp.urls')), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
