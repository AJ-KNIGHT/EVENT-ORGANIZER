# Generated by Django 5.1.4 on 2024-12-30 17:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("eventapp", "0005_booking_payment_method"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="booking",
            name="payment_method",
        ),
        migrations.RemoveField(
            model_name="booking",
            name="payment_status",
        ),
        migrations.RemoveField(
            model_name="booking",
            name="total_amount",
        ),
        migrations.AlterField(
            model_name="booking",
            name="booking_date",
            field=models.DateTimeField(),
        ),
    ]
