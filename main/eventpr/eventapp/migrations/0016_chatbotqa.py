# Generated by Django 5.1.4 on 2025-03-12 13:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("eventapp", "0015_alter_booking_venue"),
    ]

    operations = [
        migrations.CreateModel(
            name="ChatbotQA",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("question", models.CharField(max_length=255, unique=True)),
                ("answer", models.TextField()),
                (
                    "keywords",
                    models.CharField(
                        help_text="Comma-separated keywords for matching",
                        max_length=255,
                    ),
                ),
            ],
        ),
    ]
