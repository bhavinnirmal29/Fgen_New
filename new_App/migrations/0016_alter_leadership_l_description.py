# Generated by Django 4.2.14 on 2024-07-31 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("new_App", "0015_alter_leadership_l_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="leadership",
            name="l_description",
            field=models.CharField(max_length=1000),
        ),
    ]