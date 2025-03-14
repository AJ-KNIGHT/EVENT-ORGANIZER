# Generated by Django 5.1.7 on 2025-03-12 20:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("eventapp", "0022_venue"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventLocation",
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
                ("name", models.CharField(blank=True, max_length=255)),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
            ],
        ),
    ]
