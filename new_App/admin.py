from django.contrib import admin
from .models import ContactMessage, Programs, Leadership,NewsletterSubscriber

# Register your models here.

admin.site.register(ContactMessage)
admin.site.register(Programs)
admin.site.register(Leadership)
admin.site.register(NewsletterSubscriber)

