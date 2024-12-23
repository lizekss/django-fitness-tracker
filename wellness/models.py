from django.db import models
from user.models import User


class FitnessActivity(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="fitness_logs")
    activity_type = models.CharField(max_length=255)
    duration_minutes = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)
    calories = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.activity_type} ({self.duration_minutes} min) by {self.user}"

    class Meta:
        verbose_name_plural = 'Fitness activities'


class Meal(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="meal_logs")
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    calories = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Meal by {self.user} on {self.date}"


class SleepLog(models.Model):
    QUALITY_CHOICES = [
        ("poor", "Poor"),
        ("moderate", "Moderate"),
        ("good", "Good"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sleep_logs")
    hours = models.DecimalField(max_digits=4, decimal_places=2)
    quality = models.CharField(
        max_length=50, choices=QUALITY_CHOICES, blank=True, null=True)
    bedtime = models.TimeField(blank=True, null=True)
    wakeup_time = models.TimeField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.hours} hours of sleep by {self.user}"
