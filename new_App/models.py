from django.db import models

# Create your models here.
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"
    
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
    l_description = models.CharField(max_length=200)
    l_imagename = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.l_name} - ({self.l_description})"
    
    
    
from django.db import models

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
