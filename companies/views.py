from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
# from drf_api.permissions import IsOwnerOrReadOnly
from .models import Company
from .serializers import CompanySerializer


class CompanyList(generics.ListCreateAPIView):
    """
    List all companies or if logged in, create a company to submit
    for approval by admin.
    The perform_create method associates the company with the logged in user.
    """

    serializer_class = CompanySerializer
    # No permissions set as all users can view the list of companies
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
    # creates form for admin editing matching to serializer fields
    serializer_class = CompanySerializer
    # Sets the permission classes attribute
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Company.objects.annotate(
        endorsements_count=Count('endorsed_company__owner', distinct=True),
        comments_count=Count('comment', distinct=True),
    ).order_by('-created_on')
