from django.core.management.base import BaseCommand
from eventapp.models import Event, Booking, EventCustomization, EventLocation  # Change `events` to `eventapp`
from decimal import Decimal

class Command(BaseCommand):
    help = "Reset events, bookings, and locations based on new logic"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("🚀 Starting event reset process..."))

        # 1️⃣ Delete all old bookings and linked data
        Booking.objects.all().delete()
        EventCustomization.objects.all().delete()
        EventLocation.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("✅ Deleted all old bookings, customizations, and locations."))

        # 2️⃣ Delete old events
        Event.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("✅ Deleted all old events."))

        # 3️⃣ Create new events (admin will later add correct available dates)
        new_events = [
            Event(
                name="Wedding Ceremony",
                slug="wedding-ceremony",
                desc="A perfect wedding experience with custom venue selection.",
                estimated_price=Decimal("10000.00")
            ),
            Event(
                name="Corporate Conference",
                slug="corporate-conference",
                desc="A professional conference setup with flexible venue choices.",
                estimated_price=Decimal("8000.00")
            ),
            Event(
                name="Birthday Celebration",
                slug="birthday-celebration",
                desc="A customizable birthday party with decorations and catering.",
                estimated_price=Decimal("7000.00")
            ),
        ]
        Event.objects.bulk_create(new_events)
        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(new_events)} new events."))

        # 4️⃣ Confirm Reset
        self.stdout.write(self.style.SUCCESS("🎉 Event reset process completed successfully!"))
