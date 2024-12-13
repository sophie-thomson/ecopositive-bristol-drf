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
    is_owner = serializers.SerializerMethodField()
    endorsed_company_name = serializers.ReadOnlyField(
        source='endorsed_company.name'
    )
    endorsed_company_owner = serializers.ReadOnlyField(
        source='endorsed_company.owner.username'
    )

    def get_is_owner(self, obj):
        # context passed to each request in get and put views
        request = self.context['request']
        # returns true if the user is == the company's owner
        return request.user == obj.owner

    class Meta:
        model = Endorsement
        fields = [
            'id',
            'owner',
            'is_owner',
            'endorsed_company',
            'endorsed_company_name',
            'endorsed_company_owner',
            'created_on',
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })
