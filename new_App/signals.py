# Fgen_New/new_App/signals.py
# signals.py
from django.core.mail import EmailMessage
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import PDFDocument, NewsletterSubscriber
from django.conf import settings

@receiver(post_save, sender=PDFDocument)
def send_pdf_notification(sender, instance, created, **kwargs):
    if created:
        # Construct email content
        subject = 'New Newsletter Available'
        
        # Access the Cloudinary URL using `.url`
        file_url = instance.file.url
        message = f'A new Newsletter titled "{instance.title}" has been uploaded. You can view it here: {file_url}'
        
        from_email = settings.DEFAULT_FROM_EMAIL

        # Retrieve all subscribers
        subscribers = NewsletterSubscriber.objects.all()

        # Send email to each subscriber
        for subscriber in subscribers:
            email = EmailMessage(
                subject,
                message,
                from_email,
                [subscriber.email]
            )
            email.send()