# Generated by Django 5.1.1 on 2024-10-21 20:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PaymentTransaction",
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
                ("app_trans_id", models.CharField(max_length=255, unique=True)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("status", models.CharField(default="pending", max_length=50)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
