from celery import shared_task

from insights.utils import generate_personalized_insights


@shared_task
def insights_task(user_id, days=7):
    return generate_personalized_insights(user_id, days)
