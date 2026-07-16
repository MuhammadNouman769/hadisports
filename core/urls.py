# core/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('nested_admin/', include('nested_admin.urls')),
    path('admin/', admin.site.urls),
    path('', include('apps.products.urls')),
    path('', include('apps.main.urls')),
    path('', include('apps.contact.urls')),
]

# ============================================================
# SERVE STATIC & MEDIA FILES IN DEVELOPMENT
# ============================================================
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ============================================================
# ERROR HANDLERS
# ============================================================
handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'