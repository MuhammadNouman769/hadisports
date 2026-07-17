# apps/main/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from apps.testimonials.models.testimonial import Testimonial

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'client_image_preview',
        'client_name',
        'client_profession',
        'rating_display',
        'testimonial_preview',
        'display_order',
        'is_featured',
        'is_active',
        'created_at',
    )
    
    list_filter = (
        'is_featured',
        'is_active',
        'rating',
        'created_at',
    )
    
    search_fields = (
        'client_name',
        'client_profession',
        'testimonial_text',
    )
    
    list_editable = (
        'display_order',
        'is_featured',
        'is_active',
    )
    
    readonly_fields = (
        'created_at',
        'updated_at',
        'client_image_preview',
    )
    
    fieldsets = (
        ('Client Information', {
            'fields': (
                'client_name',
                'client_profession',
                'client_image',
                'client_image_preview',
            )
        }),
        ('Testimonial', {
            'fields': (
                'testimonial_text',
                'rating',
            )
        }),
        ('Settings', {
            'fields': (
                'display_order',
                'is_featured',
                'is_active',
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        }),
    )
    
    ordering = ('display_order', '-created_at')
    list_per_page = 20
    save_on_top = True
    
    def rating_display(self, obj):
        """Display stars in admin"""
        filled = '★' * obj.rating
        empty = '☆' * (5 - obj.rating)
        return mark_safe(f'<span style="color: #f39c12; font-size: 16px;">{filled}{empty}</span>')
    rating_display.short_description = 'Rating'
    
    def client_image_preview(self, obj):
        """Display client image preview in admin"""
        if obj.client_image and obj.client_image.url:
            return mark_safe(
                f'<img src="{obj.client_image.url}" width="50" height="50" style="object-fit:cover; border-radius:50%;">'
            )
        return mark_safe('<span style="color: #999;">No image</span>')
    client_image_preview.short_description = 'Image'
    
    def testimonial_preview(self, obj):
        """Preview testimonial text"""
        if len(obj.testimonial_text) > 60:
            return obj.testimonial_text[:60] + '...'
        return obj.testimonial_text
    testimonial_preview.short_description = 'Testimonial'
    
    actions = (
        'activate_testimonials',
        'deactivate_testimonials',
        'mark_featured',
        'remove_featured',
    )
    
    @admin.action(description='Activate selected testimonials')
    def activate_testimonials(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} testimonial(s) activated.')
    
    @admin.action(description='Deactivate selected testimonials')
    def deactivate_testimonials(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} testimonial(s) deactivated.')
    
    @admin.action(description='Mark selected as featured')
    def mark_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} testimonial(s) marked as featured.')
    
    @admin.action(description='Remove featured')
    def remove_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} testimonial(s) updated.')