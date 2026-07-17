from django.contrib import admin
from .models import NewsletterSubscriber

from django.utils.safestring import mark_safe
from apps.main.models import HeroBanner



@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('email',)
    list_editable = ('is_active',)



@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'image_preview',
        'title',
        'display_order',
        'is_active',
    )
    
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    list_editable = ('display_order', 'is_active')
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'description')
        }),
        ('Image', {
            'fields': ('image', 'image_preview')
        }),
        ('Button', {
            'fields': ('button_text',)  
        }),
        ('Settings', {
            'fields': ('display_order', 'is_active')
        }),
    )
    
    readonly_fields = ('image_preview',)
    ordering = ('display_order', '-created_at')
    
    def image_preview(self, obj):
        if obj and obj.image and obj.image.url:
            return mark_safe(
                f'<img src="{obj.image.url}" width="150" height="80" style="object-fit:cover; border-radius:8px;">'
            )
        return mark_safe('<span style="color: #999;">No image</span>')
    image_preview.short_description = 'Preview'    