from django.db.models import Q
from rest_framework import serializers
from .models import Company
from ..users.models import User


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
        )


class CompanySerializer(serializers.ModelSerializer):
    owner = OwnerSerializer()

    class Meta:
        model = Company
        fields = (
            'id',
            'name',
            'slug',
            'industry',
            'description',
            'address',
            'contacts',
            'owner'
        )
        depth = 1


class CompanyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'name',
            'slug',
            'industry',
            'description',
            'address',
            'contacts',
        )

    def create(self, validated_data):
        company = Company.objects.create(
            owner=self.context.get("user"),
            name=validated_data.get('name'),
            slug=validated_data.get('slug'),
            industry=validated_data.get('industry'),
            description=validated_data.get('description'),
            address=validated_data.get('address'),
            contacts=validated_data.get('contacts'),
        )
        return company


class ActiveCompanyCreateSerializer(serializers.Serializer):
    company_id = serializers.IntegerField(required=True)

    def validate_company_id(self, attrs):
        user_company_ids = Company.objects.filter(
            Q(owner=self.context.get('user')) | Q(members__in=[self.context.get('user')])).values_list('pk', flat=True)
        if attrs not in user_company_ids:
            raise serializers.ValidationError("Company not found.")
        return attrs

    def update(self, instance, validated_data):
        instance.active_company = validated_data.get('company_id')
        instance.save()
        return instance
