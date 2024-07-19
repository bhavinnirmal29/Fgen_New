from django.contrib import admin
from .models import ContactMessage, Programs, Leadership

# Register your models here.

admin.site.register(ContactMessage)
admin.site.register(Programs)
admin.site.register(Leadership)
