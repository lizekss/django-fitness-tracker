from django.contrib import admin
from .models import FitnessActivity, Meal, SleepLog

@admin.register(FitnessActivity)
class FitnessActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'duration_minutes', 'calories', 'date')
    list_filter = ('user', 'activity_type', 'date')
    search_fields = ('user__username', 'activity_type')
    readonly_fields = ('date',)
    ordering = ('-date',)

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'calories', 'date')
    list_filter = ('user', 'date')
    search_fields = ('user__username', 'description')
    readonly_fields = ('date',)
    ordering = ('-date',)

@admin.register(SleepLog)
class SleepLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'hours', 'quality', 'bedtime', 'wakeup_time', 'date')
    list_filter = ('user', 'quality', 'date')
    search_fields = ('user__username',)
    readonly_fields = ('date',)
    ordering = ('-date',)
