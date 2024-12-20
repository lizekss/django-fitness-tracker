from rest_framework import serializers
from .models import FitnessActivity, Meal, SleepLog


class FitnessActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessActivity
        fields = ['id', 'user', 'activity_type', 'duration_minutes', 'date']
        read_only_fields = ['user', 'date']


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['id', 'user', 'description', 'date']
        read_only_fields = ['user', 'date']


class SleepLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SleepLog
        fields = ['id', 'user', 'hours', 'quality',
                  'bedtime', 'wakeup_time', 'date']
        read_only_fields = ['user', 'date']
