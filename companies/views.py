from django.db.models import Count
from rest_framework import generics, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from drf_api.permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .models import Company
from .serializers import CompanySerializer


class CompanyList(generics.ListCreateAPIView):
    """
    List all companies or if logged in, create a company to submit
    for approval by admin.
    The perform_create method associates the company with the logged in user.
    """

    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    queryset = Company.objects.annotate(
        endorsements_count=Count('endorsed_company__owner', distinct=True),
        comments_count=Count('comment', distinct=True),
    ).order_by('-created_on')

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    filterset_fields = [
        # filter by credentials groups
        'credentials__group',
        # user endorsed companies
        'endorsed_company__owner'
    ]

    search_fields = [
        'name',
        'key_words',
        'excerpt',
    ]

    ordering_fields = [
        'endorsements_count',
        'comments_count',
        'credentials__group',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a company listing if you are the owner.
    """
    serializer_class = CompanySerializer
    permission_classes = [IsAdminOrReadOnly, IsOwnerOrReadOnly,]
    queryset = Company.objects.annotate(
        endorsements_count=Count('endorsed_company__owner', distinct=True),
        comments_count=Count('comment', distinct=True),
    ).order_by('-created_on')
