from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Credential


class CredentialSerializer(serializers.ModelSerializer):
    """
    Serializer for the Credential model
    """

    def get_created_on(self, obj):
        return naturaltime(obj.created_on)

    def get_updated_on(self, obj):
        return naturaltime(obj.updated_on)

    class Meta:
        model = Credential
        fields = [
            'id',
            'name',
            'group',
            'link',
            'description',
            'created_on',
            'updated_on',
        ]
