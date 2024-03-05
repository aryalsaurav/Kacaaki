from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@shared_task
def send_email_task(recipient_list,context):
    subject="Kakaaki Class Schedule"
    message_template = "layouts/emails/class_assign.html"
    message = render_to_string(message_template,context)
    plain_message = strip_tags(message)
    send_mail(
        subject,
        plain_message,
        'info@kakaaki.com',
        [recipient_list],
        html_message=message
    )