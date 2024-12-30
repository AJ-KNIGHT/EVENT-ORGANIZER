from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from paymentapp.models import Payment
from eventapp.models import Booking

CustomUser = get_user_model()

class PaymentAppTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = CustomUser.objects.create_user(username="user", password="password", email="user@example.com")

        # Create a booking
        self.booking = Booking.objects.create(
            cus_name="Jane Doe",
            cus_ph="9876543210",
            cus_email="janedoe@example.com",
            event_name="Wedding",
            event_date="2025-02-14",
            venue="Banquet Hall",
            description="A beautiful wedding ceremony."
        )

    def test_create_payment_view(self):
        # Ensure the user can create a payment
        self.client.login(username="user", password="password")
        response = self.client.post(reverse("create_payment", args=[self.booking.id]), {
            "amount": "1000.00",
            "payment_status": "Pending",
            "transaction_id": "TXN123456"
        })

        self.assertEqual(response.status_code, 302)  # Should redirect after successful creation
        self.assertEqual(Payment.objects.count(), 1)
        payment = Payment.objects.first()
        self.assertEqual(payment.amount, 1000.00)
        self.assertEqual(payment.payment_status, "Pending")
        self.assertEqual(payment.transaction_id, "TXN123456")
        self.assertEqual(payment.event_booking, self.booking)

    def test_existing_payment_error(self):
        # Create an existing payment
        Payment.objects.create(
            event_booking=self.booking,
            amount=2000.00,
            payment_status="Completed",
            transaction_id="TXN999999"
        )

        # Attempt to create another payment for the same booking
        self.client.login(username="user", password="password")
        response = self.client.post(reverse("create_payment", args=[self.booking.id]), {
            "amount": "1500.00",
            "payment_status": "Pending",
            "transaction_id": "TXN123457"
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Payment already exists for this booking.")
