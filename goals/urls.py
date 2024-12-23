from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FitnessProfileViewSet

router = DefaultRouter()
router.register(r'profiles', FitnessProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
