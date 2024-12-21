from abc import ABC, abstractmethod
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .tasks import insights_task
from celery.result import AsyncResult


class ReportView(APIView, ABC):
    """
    Abstract parent class for generating reports based on the number of days.
    """
    permission_classes = [IsAuthenticated]

    @abstractmethod
    def get_days(self):
        pass

    def get(self, request, *args, **kwargs):
        days = self.get_days()

        task = insights_task.delay(request.user.id, days)

        return Response({"task_id": task.id, "message": "Insights are being generated."})


class DailyReportView(ReportView):
    """
    API endpoint to generate and return daily personalized insights for the user.
    """

    def get_days(self):
        return 1


class WeeklyReportView(ReportView):
    """
    API endpoint to generate and return weekly personalized insights for the user.
    """

    def get_days(self):
        return 7


class MonthlyReportView(ReportView):
    """
    API endpoint to generate and return monthly personalized insights for the user.
    """

    def get_days(self):
        return 30


class CustomReportView(ReportView):
    """
    API endpoint to generate and return a custom personalized report based on the number of days.
    """

    def get_days(self):
        days = self.request.query_params.get('days')
        try:
            days = int(days)
        except (TypeError, ValueError):
            days = 7  # Default to 7 if the 'days' param is invalid or missing
        return days



class TaskResultView(APIView):
    def get(self, request, task_id, *args, **kwargs):
        task_result = AsyncResult(task_id)

        if task_result.ready():
            return Response({"status": "success", "result": task_result.result})
        else:
            return Response({"status": "processing", "message": "Task is still processing."})
