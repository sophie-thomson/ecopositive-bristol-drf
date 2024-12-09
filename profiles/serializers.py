from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        # context passed to each request in get and put views
        request = self.context['request']
        # returns true if the user is also the object's owner
        return request.user == obj.owner

    class Meta:
        model = Profile
        fields = [
            'id',
            'owner',
            'created_on',
            'updated_on',
            'first_name',
            'last_name',
            'image',
            'is_owner',
        ]
