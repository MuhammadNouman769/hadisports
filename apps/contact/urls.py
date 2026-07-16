from .views import ContactView
from django.urls import path

app_name = 'contact'

urlpatterns = [
    path('contact/', ContactView.as_view(), name='contact'),
    
]