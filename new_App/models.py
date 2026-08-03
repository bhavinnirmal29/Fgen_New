import os
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.storage import default_storage
# Create your models here.
class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('administration', 'Administration'),
        ('media_communications', 'Media & Communications'),
        ('technical_production', 'Technical & Production'),
        ('hospitality_logistics', 'Hospitality & Logistics'),
        ('ministry_spiritual_support', 'Ministry & Spiritual Support'),
        ('event_day_support', 'Event Day Support'),
        ('dancers', 'Dancers'),
        ('others', 'Others'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, blank=True, default='')
    other_subject = models.CharField(max_length=200, blank=True, default='')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

def upload_to(instance, filename):
    # Use media directory instead of static directory
    return os.path.join('images/', filename)

def upload_pdf_to(instance, filename):
    # Use media directory for PDFs
    return os.path.join('pdfs/', filename)

class Programs(models.Model):
    p_name = models.CharField(max_length=100)
    p_description = models.CharField(max_length=200)
    p_price = models.IntegerField()
    p_imagename = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.p_name} - ({self.p_description})"
    
class Leadership(models.Model):
    l_name = models.CharField(max_length=100)
    l_description = models.CharField(max_length=1000)
    l_imagename = models.ImageField(upload_to='leadership/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.l_name} - ({self.l_description})"
    

class Executive(models.Model):
    e_name = models.CharField(max_length=100)
    e_description = models.CharField(max_length=1000)
    e_imagename = models.ImageField(upload_to='executives/')
    order = models.PositiveIntegerField(default=0, help_text="Order in which this profile appears")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Executive'
        verbose_name_plural = 'Executives'

    def __str__(self):
        return f"{self.e_name} - ({self.e_description})"


class Testimonials(models.Model):
    t_name = models.CharField(max_length=100)
    t_description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.t_name} - ({self.t_description})" 
    
from django.db import models

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
class PDFDocument(models.Model):
    file = models.FileField(upload_to=upload_pdf_to)
    title = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Newsletter Document'
        verbose_name_plural = 'Newsletter Documents'

    def __str__(self):
        return self.title
    
from django.dispatch import receiver
from django.db.models.signals import post_save   

class UserPayment(models.Model):
    # app_user = models.ForeignKey(User, on_delete=models.CASCADE)
    app_user = models.EmailField()
    stripe_charge_id = models.CharField(max_length=500,default="", unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    currency = models.CharField(max_length=10, default='usd')
    payment_date = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    donation_type = models.CharField(max_length=50,default="regular")
    def __str__(self):
        return f"{self.app_user} - {self.stripe_charge_id}"
# @receiver(post_save, sender=User)
# def create_user_payment(sender, instance, created, **kwargs):
# 	if created:
# 		UserPayment.objects.create(app_user=instance)


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)
    event_date = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def is_past_event(self):
        return self.event_date < timezone.now()

class EventImage(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='events/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.description}"
  
class GoogleForm(models.Model):
    KEY_CHOICES = [
        ('programs_booking', 'Programs Page - School Presentation Booking Form'),
        ('executive_applications', 'Get Involved Page - Executive Applications Form'),
    ]
    key = models.CharField(max_length=50, choices=KEY_CHOICES, unique=True)
    title = models.CharField(max_length=200)
    form_url = models.URLField(max_length=500)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Google Form'
        verbose_name_plural = 'Google Forms'

    def __str__(self):
        return self.title


class WebData(models.Model):
    page_name = models.CharField(max_length=255)
    title = models.CharField(max_length=200)
    description_text = models.TextField()
    created_At = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.page_name} - ({self.title})"

class YouTubeVideo(models.Model):
    title = models.CharField(max_length=200)
    youtube_url = models.URLField(help_text="Enter the full YouTube URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID)")
    description = models.TextField(blank=True, help_text="Optional description of the video")
    order = models.PositiveIntegerField(default=0, help_text="Order in which videos appear in the carousel")
    is_active = models.BooleanField(default=True, help_text="Whether this video should be displayed")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'YouTube Video'
        verbose_name_plural = 'YouTube Videos'
    
    def __str__(self):
        return self.title
    
    def get_video_id(self):
        """Extract video ID from YouTube URL"""
        import re
        # Handle different YouTube URL formats
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
            r'youtube\.com\/watch\?.*v=([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.youtube_url)
            if match:
                return match.group(1)
        return None
    
    def get_embed_url(self):
        """Get the embed URL for the video"""
        video_id = self.get_video_id()
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
        return None
    
    def get_thumbnail_url(self):
        """Get the thumbnail URL for the video"""
        video_id = self.get_video_id()
        if video_id:
            return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        return None 
    