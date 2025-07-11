# Generated by Django 5.1.1 on 2024-10-18 10:51

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Notification",
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
                ("message", models.TextField()),
                (
                    "notification_type",
                    models.CharField(
                        choices=[("email", "Email"), ("SMS", "SMS")], max_length=20
                    ),
                ),
                ("sent_date", models.DateField()),
            ],
        ),
    ]
