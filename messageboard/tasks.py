from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import *
from datetime import datetime

@shared_task(name='email_notification_task')
def send_email_task(subject, body, email_address):
    email = EmailMessage(subject, body, to=[email_address])
    email.send()
    return email_address

@shared_task(name='monthly_newsletter_task')
def send_monthly_newsletter():
    subject = "Your Monthly Newsletter"

    subscribers = MessageBoard.objects.get(id=1).subscribers.filter(
        profile__newsletter_subscribed=True,
    )

    for subscriber in subscribers:
        body = render_to_string('messageboard/newsletter.html', {'name': subscriber.profile.name})
        email = EmailMessage(subject, body, to=[subscriber.email])
        email.content_subtype = 'html'
        email.send()

    return f"Newsletter sent to {len(subscribers)} subscribers for {datetime.now().strftime('%B')}."