from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from wellness.permissions import IsOwner
from .models import FitnessProfile
from .serializers import FitnessProfileSerializer

class FitnessProfileViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = FitnessProfile.objects.all()
    serializer_class = FitnessProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """
        Optionally restrict the returned fitness profiles to the currently authenticated user.
        """
        queryset = FitnessProfile.objects.all()
        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.filter(user=user)
        return queryset
