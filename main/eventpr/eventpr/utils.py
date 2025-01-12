from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_html_email(subject, recipient_list, template_name, context):
    """
    Send an HTML email using the given template and context.

    :param subject: Email subject
    :param recipient_list: List of email recipients
    :param template_name: Path to the email template
    :param context: Context dictionary to render the template
    """
    html_message = render_to_string(template_name, context)
    send_mail(
        subject=subject,
        message='',  # Leave plain text empty to prioritize HTML
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False,
        html_message=html_message,
    )
