# from django.db.models import Count
from rest_framework import generics
# from django_filters.rest_framework import DjangoFilterBackend
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # filterset_fields = [
    #     # 'owner__endorser__endorsed__profile',
    # ]

    # ordering_fields = [
    #     'companies_count',
    #     'endorsements_count',
    #     'endorsers_count',
    #     'owner__endorser__created_at',
    #     'owner__endorsed__created_at',
    # ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    # Sets the permission classes attribute
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
