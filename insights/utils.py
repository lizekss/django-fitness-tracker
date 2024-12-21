from django.db.models import Sum, Avg, Count
from datetime import timedelta
from django.utils.timezone import now

from user.models import User
from wellness.models import FitnessActivity, Meal, SleepLog
from django.db.models.functions import TruncDate, TruncDay


def generate_personalized_insights(user_id, days=7):
    """
    Generate personalized insights based on the user's logged wellness data, focusing on daily averages.
    """
    one_week_ago = now().date() - timedelta(days=days)
    user = User.objects.get(id=user_id)
    # fetch data for the time period
    fitness_logs = FitnessActivity.objects.filter(user=user, date__gte=one_week_ago)
    meals = Meal.objects.filter(user=user, date__gte=one_week_ago)
    sleep_logs = SleepLog.objects.filter(user=user, date__gte=one_week_ago)

    fitness_stats = fitness_logs.aggregate(
        avg_time_per_day=Sum('duration_minutes') / Count('date', distinct=True),
        avg_calories_per_day=Sum('calories') / Count('date', distinct=True)
    )

    most_common_activity = (
        fitness_logs
        .values('activity_type')
        .annotate(count=Count('activity_type'))
        .order_by('-count')
        .first()
    )

    meal_stats = meals.aggregate(
        avg_calories_per_day=Sum('calories') / Count('date', distinct=True)
    )

    sleep_stats = sleep_logs.aggregate(
        avg_sleep_per_day=Sum('hours') / Count('date', distinct=True)
    )

    sleep_quality_counts = (
        sleep_logs
        .values('quality')
        .annotate(count=Count('quality'))
    )

    # construct the insights
    insights = {
        "fitness": {
            "average_time_per_day": fitness_stats.get('avg_time_per_day', 0),
            "average_calories_burned_per_day": fitness_stats.get('avg_calories_per_day', 0),
            "most_common_activity": most_common_activity.get('activity_type') if most_common_activity else None,
        },
        "meals": {
            "average_calories_consumed_per_day": meal_stats.get('avg_calories_per_day', 0),
        },
        "sleep": {
            "average_sleep_hours_per_day": sleep_stats.get('avg_sleep_per_day', 0),
            "quality_counts": list(sleep_quality_counts),
        },
    }

    return insights
