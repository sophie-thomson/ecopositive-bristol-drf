from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    is_staff = serializers.ReadOnlyField()
    endorsements_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Profile
        fields = [
            'id',
            'owner',
            'is_owner',
            'is_staff',
            'created_on',
            'updated_on',
            'first_name',
            'last_name',
            'image',
            'endorsements_count',
        ]
