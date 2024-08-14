import os
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

def upload_to(instance, filename):
    return os.path.join('new_App/static/assets/images/', filename)

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
    l_imagename = models.ImageField(upload_to=upload_to)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.l_name} - ({self.l_description})"
    

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
    file = models.FileField(upload_to='pdfs/')
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
    image = models.ImageField(upload_to=upload_to)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.description}"
  
class WebData(models.Model):
    page_name = models.CharField(max_length=255)
    title = models.CharField(max_length=200)
    description_text = models.TextField()
    created_At = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.page_name} - ({self.title})"
    