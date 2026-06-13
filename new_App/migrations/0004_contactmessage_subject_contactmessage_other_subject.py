from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new_App', '0003_alter_eventimage_image_alter_leadership_l_imagename'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmessage',
            name='subject',
            field=models.CharField(
                blank=True,
                choices=[
                    ('administration', 'Administration'),
                    ('media_communications', 'Media & Communications'),
                    ('technical_production', 'Technical & Production'),
                    ('hospitality_logistics', 'Hospitality & Logistics'),
                    ('ministry_spiritual_support', 'Ministry & Spiritual Support'),
                    ('event_day_support', 'Event Day Support'),
                    ('dancers', 'Dancers'),
                    ('others', 'Others'),
                ],
                default='',
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name='contactmessage',
            name='other_subject',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
