from django.contrib import admin
from .models import ContactMessage, Programs, Leadership,NewsletterSubscriber,PDFDocument,UserPayment, Event, WebData, Testimonials, YouTubeVideo
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

@admin.register(YouTubeVideo)
class YouTubeVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')
    list_filter = ('is_active', 'created_at')
    ordering = ('order', 'created_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'youtube_url', 'description')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )


    