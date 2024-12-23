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


class WeeklyThrottle(AbstractTimeBasedThrottle):
    scope = 'weekly'


class MonthlyThrottle(AbstractTimeBasedThrottle):
    scope = 'monthly'


class DailyThrottle(AbstractTimeBasedThrottle):
    scope = 'daily'
