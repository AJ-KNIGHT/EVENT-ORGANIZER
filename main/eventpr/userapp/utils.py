from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_html_email(subject, template_name, context, recipient_list):
    """
    Sends an HTML email using a Django template.
    """
    message = render_to_string(template_name, context)
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
        html_message=message,  # Ensure it's an HTML email
    )
