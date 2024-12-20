from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import FitnessActivity, Meal, SleepLog
from .serializers import FitnessActivitySerializer, MealSerializer, SleepLogSerializer

class FitnessActivityViewSet(viewsets.ModelViewSet):
    serializer_class = FitnessActivitySerializer
    queryset = FitnessActivity.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    queryset = Meal.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SleepLogViewSet(viewsets.ModelViewSet):
    serializer_class = SleepLogSerializer
    queryset = SleepLog.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

