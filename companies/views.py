from django.http import Http404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Company
from .serializers import CompanySerializer


class CompanyList(APIView):
    """
    List all companies.
    """
    
    serializer_class = CompanySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    
    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(
            companies, many= True, context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = CompanySerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
