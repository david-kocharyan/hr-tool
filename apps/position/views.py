import pandas as pd
from django.http import HttpResponse

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend

from apps.company.models import Company
from apps.position.models import Position
from apps.position.serializers import PositionSerializer, PositionCreateSerializer


class PositionView(viewsets.ModelViewSet):
    serializer_class = PositionSerializer
    queryset = Position.objects.all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['name', 'skill']
    ordering_fields = ['created_at', 'number']
    filter_fields = ['name', 'number']

    def get_queryset(self):
        return Position.objects.filter(company_id=self.request.user.active_company).order_by('-created_at')

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            serializer_class = PositionCreateSerializer
        else:
            serializer_class = PositionSerializer
        return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)

        position = serializer.create(validated_data=serializer.validated_data)
        return Response({'result': self.serializer_class(position).data}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path="export", url_name="export_position", )
    def export_positions(self, request, *args, **kwargs):
        company = Company.objects.filter(pk=request.user.active_company).first()
        positions = Position.objects.filter(pk__in=request.data.get('id_list')).values('name', 'description', 'skill',
                                                                                       'number', )
        if not positions:
            return Response({"message": "Positions not found."}, status=status.HTTP_400_BAD_REQUEST)

        dataframe = pd.DataFrame(list(positions))
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=f"{company.name}_positions.csv"'
        dataframe.to_csv(response, encoding='utf-8', header=["Name", "Description", "Skill", "Number"])
        return response
