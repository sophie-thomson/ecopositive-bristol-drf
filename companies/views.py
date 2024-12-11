from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Company
from .serializers import CompanySerializer


class CompanyList(generics.ListCreateAPIView):
    """
    List all companies or if logged in, create a company to submit
    for approval by admin.
    The perform_create method associates the company with the logged in user.
    """

    serializer_class = CompanySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = Company.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a company listing if you are the owner.
    """
    # creates form for admin editing matching to serializer fields
    serializer_class = CompanySerializer
    # Sets the permission classes attribute
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Company.objects.all()
