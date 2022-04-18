from django.conf import settings
from rest_framework import serializers

from .models import Applicant
from ..company.models import Company
from ..position.models import Position


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            "id",
            "name",
        )


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = (
            "id",
            "name",
        )


class ApplicantSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    position_applied = PositionSerializer()
    cv = serializers.SerializerMethodField()

    class Meta:
        model = Applicant
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "gender",
            "country",
            "dob",
            "level",
            "skill",
            "comment",
            "status",
            "company",
            "position_applied",
            "cv",
        )
        depth = 1

    def get_cv(self, obj):
        return f"{settings.BASE_URL}/media/{obj.cv}"


class ApplicantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = (
            "position_applied",
            "first_name",
            "last_name",
            "email",
            "phone",
            "gender",
            "country",
            "dob",
            "level",
            "skill",
            "comment",
            "status",
            "cv",
        )

    def create(self, validated_data):
        current_user = self.context.get('user')
        applicant = Applicant.objects.create(
            company_id=current_user.active_company,
            position_applied=validated_data.get('position_applied'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data.get('email'),
            phone=validated_data.get('phone'),
            gender=validated_data.get('gender'),
            country=validated_data.get('country'),
            dob=validated_data.get('dob'),
            level=validated_data.get('level'),
            skill=validated_data.get('skill'),
            comment=validated_data.get('comment'),
            status=validated_data.get('status'),
            cv=validated_data.get('cv'),
        )
        return applicant


class ApplicantCvUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ("cv",)

    def update(self, instance, validated_data):
        instance.cv = validated_data['cv']
        instance.save()
