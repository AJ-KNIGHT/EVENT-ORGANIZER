from django.core.management.base import BaseCommand
from eventapp.models import EventCustomization, Booking

class Command(BaseCommand):
    help = 'Deletes all EventCustomizations and Bookings'

    def handle(self, *args, **kwargs):
        # Delete all EventCustomization records
        EventCustomization.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all EventCustomizations'))

        # Delete all Booking records
        Booking.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all Bookings'))
