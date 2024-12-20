from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils import generate_personalized_insights

class WeeklyReportView(APIView):
    """
    API endpoint to generate and return weekly personalized insights for the user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        insights = generate_personalized_insights(request.user)
        return Response(insights)
