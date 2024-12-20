from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FitnessActivityViewSet, MealViewSet, SleepLogViewSet

router = DefaultRouter()
router.register(r'fitness', FitnessActivityViewSet)
router.register(r'meals', MealViewSet)
router.register(r'sleep', SleepLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
