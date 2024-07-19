# Generated by Django 4.2.14 on 2024-07-19 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("new_App", "0004_programs_p_imagename"),
    ]

    operations = [
        migrations.CreateModel(
            name="Leadership",
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
                ("l_name", models.CharField(max_length=100)),
                ("l_description", models.CharField(max_length=200)),
                ("l_imagename", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
