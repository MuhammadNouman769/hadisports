from django.contrib import admin
from apps.whatspp.models.whatsapp_setting import SiteSetting


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    fieldsets = (
        ('WhatsApp Settings', {
            'fields': ('whatsapp_number', 'whatsapp_message_template'),
        }),
        ('Site Information', {
            'fields': ('site_name', 'site_email', 'site_phone', 'site_address'),
        }),
    )
    
    def has_add_permission(self, request):
        """Only allow one settings instance"""
        if SiteSetting.objects.exists():
            return False
        return True
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of settings"""
        return False