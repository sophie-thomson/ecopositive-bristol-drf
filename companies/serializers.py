from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    def validate_logo(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size too large, please use an image smaller than 2MB'
            )
        if value.image.width > 1500:
            raise serializers.ValidationError(
                'Image width must be less than 1500px'
            )
        if value.image.height > 1500:
            raise serializers.ValidationError(
                'Image height must be less than 1500px'
            )
        return value

    def get_is_owner(self, obj):
        # context passed to each request in get and put views
        request = self.context['request']
        # returns true if the user is also the object's owner
        return request.user == obj.owner

    class Meta:
        model = Company
        fields = [
            'id',
            'owner',
            'profile_id',
            'profile_image',
            'name',
            'logo',
            'website_url',
            'excerpt',
            'description',
            'credentials',
            'key_words',
            'contact_name',
            'contact_email',
            'role',
            'created_on',
            'updated_on',
            'is_owner',
        ]
