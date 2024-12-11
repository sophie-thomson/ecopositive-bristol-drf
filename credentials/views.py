from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Credential
from .serializers import CredentialSerializer, CredentialDetailSerializer


class CredentialList(generics.ListCreateAPIView):
    """
    List credentials.
    """
    serializer_class = CredentialSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Credential.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CredentialDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a credential, or update or delete it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CredentialDetailSerializer
    queryset = Credential.objects.all()
