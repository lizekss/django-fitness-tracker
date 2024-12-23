from rest_framework import serializers

from goals.models import FitnessProfile
from .api_utils import get_available_activities, get_calories_burned, get_available_activities_example, \
    get_meal_calories
from .models import FitnessActivity, Meal, SleepLog


class FitnessActivitySerializer(serializers.ModelSerializer):
    activity_type_choices = get_available_activities_example()
    activity_type = serializers.ChoiceField(
        choices=[(activity, activity) for activity in activity_type_choices])

    class Meta:
        model = FitnessActivity
        fields = ['user', 'activity_type',
                  'duration_minutes', 'date', 'calories']
        read_only_fields = ['user', 'date', 'calories']

    def create(self, validated_data):
        activity_type = validated_data.get('activity_type')
        duration_minutes = validated_data.get('duration_minutes')

        user = self.context['request'].user
        try:
            fitness_profile = FitnessProfile.objects.get(user_id=user.id)
            user_weight = fitness_profile.weight
        except FitnessProfile.DoesNotExist:
            user_weight = None

        calories_burned = get_calories_burned(activity_type, duration_minutes, user_weight)

        validated_data['calories'] = calories_burned
        return FitnessActivity.objects.create(**validated_data)


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['id', 'user', 'description', 'date', 'calories']
        read_only_fields = ['user', 'date', 'calories']

    def validate(self, data):
        meal_description = data.get('description')

        calories = get_meal_calories(meal_description)

        data['calories'] = calories
        return data


class SleepLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SleepLog
        fields = ['id', 'user', 'hours', 'quality',
                  'bedtime', 'wakeup_time', 'date']
        read_only_fields = ['user', 'date']
