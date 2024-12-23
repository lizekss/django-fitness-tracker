from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model

from insights.utils import generate_personalized_insights


@shared_task
def insights_task(user_id, days=7):
    return generate_personalized_insights(user_id, days)


User = get_user_model()

@shared_task
def send_weekly_insights():
    users = User.objects.filter(is_subscribed_to_weekly_emails=True)
    for user in users:
        weekly_averages = generate_personalized_insights(user.id)
        subject = "Your Weekly Fitness Insights"
        html_message = render_to_string('emails/weekly_insight.html', {
            'insight': weekly_averages,
        })
        plain_message = strip_tags(html_message)
        from_email = 'noreply@yourdomain.com'
        to_email = user.email

        send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
