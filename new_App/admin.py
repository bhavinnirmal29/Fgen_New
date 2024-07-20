from django.contrib import admin
from .models import ContactMessage, Programs, Leadership,NewsletterSubscriber,PDFDocument

# Register your models here.

admin.site.register(ContactMessage)
admin.site.register(Programs)
admin.site.register(Leadership)
@admin.register(PDFDocument)
class PDFDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title',)
    def get_model_name(self):
        return 'Newsletter Documents'

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)


