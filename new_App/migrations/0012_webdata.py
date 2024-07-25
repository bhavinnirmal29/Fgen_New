# Generated by Django 4.2.14 on 2024-07-25 00:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("new_App", "0011_event"),
    ]

    operations = [
        migrations.CreateModel(
            name="WebData",
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
                ("page_name", models.CharField(max_length=255)),
                ("title", models.CharField(max_length=200)),
                ("description_text", models.TextField()),
                ("created_At", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
