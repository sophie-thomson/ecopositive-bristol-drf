from rest_framework import generics
# from drf_api.permissions import IsOwnerOrReadOnly
from .models import Credential
from .serializers import CredentialSerializer


class CredentialList(generics.ListCreateAPIView):
    """
    List credentials.
    """
    serializer_class = CredentialSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Credential.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
