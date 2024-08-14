from django.contrib import admin
from .models import ContactMessage, Programs, Leadership,NewsletterSubscriber,PDFDocument,UserPayment, Event, WebData, Testimonials
from .models import Event, EventImage
# Register your models here.
class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1

class EventAdmin(admin.ModelAdmin):
    inlines = [EventImageInline]
    
admin.site.register(ContactMessage)
admin.site.register(Programs)
admin.site.register(Leadership)
admin.site.register(UserPayment)
admin.site.register(Event)
admin.site.register(WebData)
admin.site.register(Testimonials)
admin.site.register(EventImage)
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



    