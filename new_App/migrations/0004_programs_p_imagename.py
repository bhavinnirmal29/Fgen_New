# Generated by Django 4.2.14 on 2024-07-19 05:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("new_App", "0003_programs"),
    ]

    operations = [
        migrations.AddField(
            model_name="programs",
            name="p_imagename",
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]