from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    endorsements_count = serializers.ReadOnlyField()
    is_staff = serializers.SerializerMethodField()

    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size too large, please use an image smaller than 2MB'
            )
        if value.image.width > 1000:
            raise serializers.ValidationError(
                'Image width must be less than 1000px'
            )
        if value.image.height > 1000:
            raise serializers.ValidationError(
                'Image height must be less than 1000px'
            )
        return value

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
            'created_on',
            'updated_on',
            'first_name',
            'last_name',
            'image',
            'endorsements_count',
            'is_staff',
        ]
