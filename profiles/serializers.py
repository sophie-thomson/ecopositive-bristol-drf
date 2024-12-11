from rest_framework import serializers
from .models import Profile
# from endorsements.models import Endorsement


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    # endorser_id = serializers.SerializerMethodField()
    # companies_count = serializers.ReadOnlyField()
    # endorsements_count = serializers.ReadOnlyField()
    # endorser_count = serializers.ReadOnlyField()
    # endorsed_id = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    # def get_endorser_id(self, obj):
    #     user = self.context['request'].user
    #     if user.is_authenticated:
    #         endorser = Endorsement.objects.filter(
    #             # should 'endorsed=obj.owner' be =obj.company?
    #             owner=user, endorsed=obj.owner
    #         ).first()
    #         print(endorser)
    #         return endorser.id if endorser else None
    #     return None

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
