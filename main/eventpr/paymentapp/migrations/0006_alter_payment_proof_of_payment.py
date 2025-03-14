# Generated by Django 5.1.4 on 2024-12-28 15:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("paymentapp", "0005_payment_payment_method"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="proof_of_payment",
            field=models.ImageField(
                default="no proof provided", upload_to="pic/payment_proof/"
            ),
        ),
    ]
