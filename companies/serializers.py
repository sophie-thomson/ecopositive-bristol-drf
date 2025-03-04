from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Company
from endorsements.models import Endorsement


class CompanySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    endorsing_users = serializers.SerializerMethodField()
    endorsements_count = serializers.ReadOnlyField()
    endorsement_id = serializers.SerializerMethodField()
    comments_count = serializers.ReadOnlyField()
    owner_profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    owner_profile_image = serializers.ReadOnlyField(
        source='owner.profile.image.url'
    )
    is_staff = serializers.SerializerMethodField()

    def validate_logo(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size too large, please use an image smaller than 2MB'
            )
        if value.image.width > 800:
            raise serializers.ValidationError(
                'Image width must be less than 800px'
            )
        if value.image.height > 800:
            raise serializers.ValidationError(
                'Image height must be less than 800px'
            )
        return value

    def get_is_owner(self, obj):
        # context passed to each request in get and put views
        request = self.context['request']
        # returns true if the user is == the company's owner
        return request.user == obj.owner

    def get_is_staff(self, obj):
        request = self.context['request']
        return request.user.is_staff

    def get_endorsement_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            endorsement = Endorsement.objects.filter(
                owner=user, endorsed_company=obj
            ).first()
            return endorsement.id if endorsement else None
        return None

    # **This method was written with Code Institute Tutor support 12/12/24**
    def get_endorsing_users(self, obj):
        users = User.objects.filter(endorsing_user__endorsed_company=obj.id)
        return users.values('id', 'username')

    class Meta:
        model = Company
        fields = [
            'id',
            'owner',
            'is_owner',
            'owner_profile_id',
            'owner_profile_image',
            'name',
            'logo',
            'website_url',
            'street',
            'city',
            'postcode',
            'phone',
            'excerpt',
            'description',
            'key_words',
            'contact_name',
            'contact_email',
            'role',
            'created_on',
            'updated_on',
            'credentials',
            'endorsing_users',
            'endorsements_count',
            'endorsement_id',
            'comments_count',
            'approved',
            'is_staff',
        ]
