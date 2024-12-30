from django.urls import path
from . import views

urlpatterns = [
    path('payment/<int:booking_id>/', views.payment_view, name='payment'),
    path('payment/verify/', views.payment_verify, name='payment_verify'),  # For verifying Razorpay payment
]
