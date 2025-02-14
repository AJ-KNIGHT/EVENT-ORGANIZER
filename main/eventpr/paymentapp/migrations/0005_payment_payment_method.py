# Generated by Django 5.1.4 on 2024-12-28 08:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("paymentapp", "0004_payment_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="payment_method",
            field=models.CharField(
                choices=[
                    ("UPI", "UPI"),
                    ("Bank Transfer", "Bank Transfer"),
                    ("Cash", "Cash"),
                    ("Online", "Online Payment Gateway"),
                ],
                default="UPI",
                max_length=50,
            ),
        ),
    ]
