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
        message = f'A new Newsletter titled "{instance.title}" has been uploaded. Check it out!'
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
            email.attach_file(instance.file.path)
            email.send()
