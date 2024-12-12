from django.db import IntegrityError
from rest_framework import serializers
from .models import Endorsement


class EndorsementSerializer(serializers.ModelSerializer):
    """
    Serializer for the Endorsement model
    Create method handles the unique constraint on 'owner'
    and 'endorsed_company'
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    endorsed_company_name = serializers.ReadOnlyField(
        source='endorsed_company.name'
    )

    class Meta:
        model = Endorsement
        fields = [
            'id',
            'owner',
            'endorsed_company',
            'endorsed_company_name',
            'created_on',
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'possible duplicate'})
