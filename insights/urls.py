from django.urls import path
from .views import WeeklyReportView, CustomReportView, MonthlyReportView, DailyReportView

urlpatterns = [
    path('daily-report/', DailyReportView.as_view(), name='daily-report'),
    path('weekly-report/', WeeklyReportView.as_view(), name='weekly-report'),
    path('monthly-report/', MonthlyReportView.as_view(), name='monthly-report'),
    path('report/', CustomReportView.as_view(), name='custom-report'),
]
