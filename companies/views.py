from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Company
from .serializers import CompanySerializer


class CompanyList(APIView):
    """
    List all companies.
    """
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(
            profiles, many= True, context={'request': request}
        )
        return Response(serializer.data)
