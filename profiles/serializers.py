from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    admin_access = serializers.ReadOnlyField()
    endorsements_count = serializers.ReadOnlyField()
    is_staff = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_is_staff(self, obj):
        request = self.context['request']
        return request.user.is_staff

    class Meta:
        model = Profile
        fields = [
            'id',
            'owner',
            'is_owner',
            'admin_access',
            'created_on',
            'updated_on',
            'first_name',
            'last_name',
            'image',
            'endorsements_count',
            'is_staff',
        ]
