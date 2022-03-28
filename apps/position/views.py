from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend

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
        elif self.action == 'export_positions':
            serializer_class = ""
        else:
            serializer_class = PositionSerializer
        return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)

        position = serializer.create(validated_data=serializer.validated_data)
        return Response({'result': self.serializer_class(position).data}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path="export", url_name="export_positions", )
    def export_positions(self, request, *args, **kwargs):
        print(request.user)
        # serializer = self.get_serializer(data=request.data, context={'user': request.user})
        # serializer.is_valid(raise_exception=True)
        # serializer.update(instance=request.user, validated_data=serializer.validated_data)
        return Response(status=status.HTTP_205_RESET_CONTENT)