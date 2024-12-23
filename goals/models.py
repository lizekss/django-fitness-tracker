
from django.db import models

from user.models import User


class FitnessProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    weight = models.FloatField(help_text="User's current weight in kilograms")
    height = models.FloatField(help_text="User's height in centimeters")
    age = models.PositiveIntegerField(help_text="User's age in years")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, help_text="User's gender")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def bmi(self):
        """
        Calculate the user's Body Mass Index (BMI).
        BMI = weight (kg) / (height (m)^2)
        """
        height_in_meters = self.height / 100  # Convert height to meters
        return self.weight / (height_in_meters ** 2)

    def __str__(self):
        return f"{self.user}'s Profile"


class FitnessGoal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='fitness_goal')

    # Weight goals
    goal_weight = models.FloatField(help_text="User's target weight in kilograms", null=True, blank=True)

    # Activity goals
    daily_steps = models.PositiveIntegerField(help_text="Target number of steps per day", null=True, blank=True)
    weekly_active_minutes = models.PositiveIntegerField(
        help_text="Target number of active minutes per week",
        null=True,
        blank=True
    )

    # Nutrition goals
    daily_calorie_intake = models.PositiveIntegerField(help_text="Target daily calorie intake in kcal", null=True,
                                                       blank=True)
    protein_target = models.FloatField(help_text="Target protein intake in grams per day", null=True, blank=True)
    carb_target = models.FloatField(help_text="Target carbohydrate intake in grams per day", null=True, blank=True)
    fat_target = models.FloatField(help_text="Target fat intake in grams per day", null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Fitness Goal for {self.user.username}"
