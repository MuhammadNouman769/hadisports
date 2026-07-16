
from apps.whatspp.models.whatsapp_setting import SiteSetting


def site_settings(request):
    """
    Context processor to add site settings to all templates
    """
    settings = SiteSetting.get_settings()
    return {
        'site_settings': settings,
    }