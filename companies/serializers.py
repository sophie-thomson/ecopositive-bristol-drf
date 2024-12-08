from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

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
            'logo',
            'name',
            'website_url',
            'excerpt',
            'description',
            # 'credentials',
            'created_on',
            'updated_on',  
            'is_owner',  
        ]