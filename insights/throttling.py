from rest_framework.throttling import SimpleRateThrottle
from datetime import timedelta
from django.utils import timezone

class AbstractTimeBasedThrottle(SimpleRateThrottle):
    """
    Abstract base class for time-based throttling.
    Child classes should define the `scope` attribute.
    """
    def get_cache_key(self, request, view):
        """
        Generate the cache key based on user ID and throttle scope.
        """
        user = request.user
        if not user.is_authenticated:
            return None
        return f"{user.pk}-{self.scope}"

    def parse_rate(self, rate):
        if rate is None:
            return (None, None)
        num, period = rate.split('/')
        num_requests = int(num)
        day_duration = 86400
        days = int(period[:-1]) if period[:-1] else 1
        return (num_requests, days * day_duration)


class WeeklyThrottle(AbstractTimeBasedThrottle):
    scope = 'weekly'
    rate = '1/7d'


class MonthlyThrottle(AbstractTimeBasedThrottle):
    scope = 'monthly'
    rate = '1/30d'


class DailyThrottle(AbstractTimeBasedThrottle):
    scope = 'daily'
    rate = '1/d'
