from django.views.generic import TemplateView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from apps.whatspp.models.whatsapp_setting import SiteSetting


class ContactView(TemplateView):
    template_name = "pages/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get site settings
        site_settings = SiteSetting.get_settings()
        context['site_settings'] = site_settings
        
        return context
    
    def post(self, request, *args, **kwargs):
        # Get form data
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Validate
        if not name or not email or not message:
            messages.error(request, 'Please fill in all required fields.')
            return self.get(request, *args, **kwargs)
        
        # Get site settings
        site_settings = SiteSetting.get_settings()
        
        # Send email
        try:
            html_message = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: #81c408; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; background: #f9f9f9; }}
                    .footer {{ background: #333; color: white; padding: 10px; text-align: center; font-size: 12px; }}
                    .field {{ margin-bottom: 15px; }}
                    .label {{ font-weight: bold; color: #555; }}
                    .value {{ padding: 5px 10px; background: white; border-radius: 4px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>📩 New Contact Form Message</h2>
                        <p>From {site_settings.site_name}</p>
                    </div>
                    <div class="content">
                        <div class="field">
                            <div class="label">👤 Name:</div>
                            <div class="value">{name}</div>
                        </div>
                        <div class="field">
                            <div class="label">📧 Email:</div>
                            <div class="value"><a href="mailto:{email}">{email}</a></div>
                        </div>
                        <div class="field">
                            <div class="label">📝 Subject:</div>
                            <div class="value">{subject or 'No Subject'}</div>
                        </div>
                        <div class="field">
                            <div class="label">💬 Message:</div>
                            <div class="value" style="white-space: pre-wrap;">{message}</div>
                        </div>
                    </div>
                    <div class="footer">
                        <p>© {site_settings.site_name} - Contact Form</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            text_message = f"""
            New Contact Form Submission
            
            Name: {name}
            Email: {email}
            Subject: {subject or 'No Subject'}
            
            Message:
            {message}
            
            ---
            Sent from {site_settings.site_name} Contact Form
            """
            
            send_mail(
                subject=f'Contact Form: {subject or "New Message"} from {name}',
                message=text_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                html_message=html_message,
                fail_silently=False,
            )
            
            messages.success(
                request, 
                '✅ Thank you for your message! We will get back to you shortly.'
            )
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Email sending error: {str(e)}")
            
            messages.error(
                request, 
                '❌ There was an error sending your message. Please try again later.'
            )
        
        return self.get(request, *args, **kwargs)