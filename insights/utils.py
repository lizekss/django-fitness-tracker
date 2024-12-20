from django.db import models
from datetime import timedelta
from django.utils.timezone import now
from wellness.models import FitnessActivity, Meal, SleepLog

def generate_personalized_insights(user, days=7):
    """
    Generate personalized insights based on the user's logged wellness data.
    """
    one_week_ago = now().date() - timedelta(days=days)
    fitness_logs = FitnessActivity.objects.filter(user=user, date__gte=one_week_ago)
    meals = Meal.objects.filter(user=user, date__gte=one_week_ago)
    sleep_logs = SleepLog.objects.filter(user=user, date__gte=one_week_ago)

    # fitness stats
    total_fitness_time = sum(log.duration_minutes for log in fitness_logs)
    most_common_activity = (
        fitness_logs.values('activity_type')
        .annotate(count=models.Count('activity_type'))
        .order_by('-count')
        .first()
    )

    # meal stats
    total_meals_logged = meals.count()

    # sleep stats
    total_sleep_hours = sum(log.hours for log in sleep_logs)
    average_sleep_hours = (
        total_sleep_hours / sleep_logs.count() if sleep_logs.count() else 0
    )
    sleep_quality_counts = sleep_logs.values('quality').annotate(count=models.Count('quality'))

    insights = {
        "fitness": {
            "total_time": total_fitness_time,
            "most_common_activity": most_common_activity['activity_type'] if most_common_activity else None,
        },
        "meals": {
            "total_meals_logged": total_meals_logged,
        },
        "sleep": {
            "total_hours": total_sleep_hours,
            "average_hours": average_sleep_hours,
            "quality_counts": sleep_quality_counts,
        },
    }

    return insights
