# Generated by Django 4.2.13 on 2024-08-25 18:19

from django.db import migrations, models
import django.utils.timezone
import new_App.models


class Migration(migrations.Migration):

    dependencies = [
        ('new_App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('event_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='EventImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=new_App.models.upload_to)),
                ('description', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Leadership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('l_name', models.CharField(max_length=100)),
                ('l_description', models.CharField(max_length=1000)),
                ('l_imagename', models.ImageField(upload_to=new_App.models.upload_to)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewsletterSubscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('subscribed_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PDFDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='pdfs/')),
                ('title', models.CharField(max_length=255)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Newsletter Document',
                'verbose_name_plural': 'Newsletter Documents',
            },
        ),
        migrations.CreateModel(
            name='Programs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_name', models.CharField(max_length=100)),
                ('p_description', models.CharField(max_length=200)),
                ('p_price', models.IntegerField()),
                ('p_imagename', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Testimonials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_name', models.CharField(max_length=100)),
                ('t_description', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_user', models.EmailField(max_length=254)),
                ('stripe_charge_id', models.CharField(default='', max_length=500, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('currency', models.CharField(default='usd', max_length=10)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('success', models.BooleanField(default=False)),
                ('donation_type', models.CharField(default='regular', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='WebData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_name', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=200)),
                ('description_text', models.TextField()),
                ('created_At', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.RemoveField(
            model_name='contactmessage',
            name='user',
        ),
    ]
