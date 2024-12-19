from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Credential


class CredentialSerializer(serializers.ModelSerializer):
    """
    Serializer for the Credential model
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    def get_created_on(self, obj):
        return naturaltime(obj.created_on)

    def get_updated_on(self, obj):
        return naturaltime(obj.updated_on)

    class Meta:
        model = Credential
        fields = [
            'id',
            'owner',
            'name',
            'group',
            'link',
            'description',
            'created_on',
            'updated_on',
        ]


class CredentialDetailSerializer(CredentialSerializer):
    """
    Serializer for the Credential model used in Detail view.
    Inherits methods and attributes (Meta) from CredentialSerializer.
    Company is a read only field so that we dont have to set it on each update
    """
    # company = serializers.ReadOnlyField(source='company.id')
