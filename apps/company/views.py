from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend

from apps.company.models import Company
from apps.company.serializers import (CompanySerializer, CompanyCreateSerializer, ActiveCompanyCreateSerializer, )


class CompanyView(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['name']
    ordering_fields = ['created_at']
    filter_fields = ['industry', 'address']

    def get_queryset(self):
        return Company.objects.filter(Q(owner=self.request.user) | Q(members__in=[self.request.user]))

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            serializer_class = CompanyCreateSerializer
        elif self.action == 'update':
            serializer_class = CompanyCreateSerializer
        elif self.action == 'active_company':
            serializer_class = ActiveCompanyCreateSerializer
        else:
            serializer_class = CompanySerializer
        return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        company = serializer.create(validated_data=serializer.validated_data)
        return Response({'result': self.serializer_class(company).data}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path="active-company", url_name="active_company", )
    def active_company(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=request.user, validated_data=serializer.validated_data)
        return Response(status=status.HTTP_205_RESET_CONTENT)
