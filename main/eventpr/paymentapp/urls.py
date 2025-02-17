from django.urls import path
from . import views
app_name = 'paymentapp'
urlpatterns = [
    path("payment/", views.payment_page, name="payment_page"),
    path("confirm/", views.confirm_payment, name="confirm_payment"),
    path("success/", views.payment_success, name="payment_success"),
]
