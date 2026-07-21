# core/views.py

from django.shortcuts import render
from django.http import HttpResponse
import logging
from django.http import FileResponse, Http404
from django.conf import settings
import os




logger = logging.getLogger(__name__)


def custom_404(request, exception):
    """Custom 404 page handler"""
    logger.error(f"404 Error: {exception}")
    
    try:
        from apps.whatspp.models.whatsapp_setting import SiteSetting
        site_settings = SiteSetting.get_settings()
    except:
        site_settings = None
    
    return render(request, '404.html', {
        'site_settings': site_settings
    }, status=404)


def custom_500(request):
    """Custom 500 page handler"""
    import traceback
    logger.error(f"500 Error: {traceback.format_exc()}")
    
    try:
        from apps.whatspp.models.whatsapp_setting import SiteSetting
        site_settings = SiteSetting.get_settings()
    except:
        site_settings = None
    
    return render(request, '500.html', {
        'site_settings': site_settings
    }, status=500)



def serve_media(request, path):
    """Serve media files in production with DEBUG=False"""
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'))
    else:
        raise Http404("File not found")    