from rest_framework import serializers

from apps.member.models import Invite
from apps.users.models import User


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'dob',
            'is_active',
            'auth_provider',
        )
        extra_kwargs = {'password': {'write_only': True}}
        depth = 1


class InviteSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def create_invitation(self, validated_data, company, uuid):
        old = Invite.objects.filter(email=validated_data.get('email')).first()
        if old:
            raise serializers.ValidationError({"old_invitation": "You already send invitation for this email"})

        invitation = Invite.objects.create(
            company=company,
            email=validated_data.get('email'),
            uuid=uuid
        )
        return invitation


class InviteActionSerializer(serializers.Serializer):
    pass