from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Company
from endorsements.models import Endorsement


class CompanySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    endorsement_id = serializers.SerializerMethodField()
    endorsed_company_id = serializers.SerializerMethodField()
    endorsing_users = serializers.SerializerMethodField()
    owner_profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    owner_profile_image = serializers.ReadOnlyField(
        source='owner.profile.image.url'
    )

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
        # returns true if the user is == the company's owner
        return request.user == obj.owner

    def get_endorsement_id(self, obj):
        # get current user from context and check if authenticated
        user = self.context['request'].user
        if user.is_authenticated:
            # filter the endorsement object
            endorsement = Endorsement.objects.filter(
                # if the logged in user is endorsing this company,
                # then an instance will be returned.
                owner=user, endorsed_company=obj.id
            ).first()
            # prints the first endorsement for each company instance
            # print(endorsement)
            return endorsement.id if endorsement else None
        return None

    def get_endorsed_company_id(self, obj):
        company_id = Endorsement.objects.filter(
            endorsed_company=obj.id
        )
        print(company_id)
        # return company_id

    # def get_endorsing_users(self, obj):
    #     endorsements = Endorsement.objects.filter(
    #         endorsed_company=obj.id
    #     )
    #     print(endorsements)
    #     print(len(endorsements))

    # **This method was written with Code Institute Tutor support 12/12/24**
    def get_endorsing_users(self, obj):
        users = User.objects.filter(endorsing_user__endorsed_company=obj.id)
        return users.values('id', 'username', 'first_name', 'last_name')

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
            'excerpt',
            'description',
            'key_words',
            'contact_name',
            'contact_email',
            'role',
            'created_on',
            'updated_on',
            'credentials',
            'endorsement_id',
            'endorsing_users',
            'endorsed_company_id',
        ]
