from rest_framework import serializers
from .models import Position
from ..company.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            "id",
            "name",
            "slug",
        )


class PositionSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = Position
        fields = (
            "id",
            "company",
            "name",
            "description",
            "skill",
            "number",

        )
        depth = 1


class PositionCreateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=60)
    description = serializers.CharField(required=True, max_length=500)
    skill = serializers.ListField(required=True, child=serializers.CharField())
    number = serializers.IntegerField(required=True, min_value=0)

    def create(self, validated_data):
        user = self.context.get('user')
        position = Position.objects.create(
            company_id=user.active_company,
            name=validated_data.get('name'),
            description=validated_data.get('description'),
            skill=validated_data.get('skill'),
            number=validated_data.get('number'),
        )
        return position
