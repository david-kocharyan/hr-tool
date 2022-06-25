import pandas as pd
from django.http import HttpResponse

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend

from apps.applicant.models import Applicant
from apps.applicant.serializers import ApplicantSerializer, ApplicantCreateSerializer, ApplicantCvUpdateSerializer
from apps.company.models import Company


class ApplicantView(viewsets.ModelViewSet):
    serializer_class = ApplicantSerializer
    queryset = Applicant.objects.all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['first_name', 'last_name', 'email', ]
    ordering_fields = ['gender', 'country', 'status', 'created_at']
    filter_fields = ['email', 'gender', 'country', 'level', 'status', ]

    def get_queryset(self):
        return Applicant.objects.filter(company_id=self.request.user.active_company).order_by('-created_at')

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            serializer_class = ApplicantCreateSerializer
        else:
            serializer_class = ApplicantSerializer
        return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        applicant = serializer.create(validated_data=serializer.validated_data)
        return Response({'result': self.serializer_class(applicant).data}, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        applicant = self.get_object()
        data = request.data
        if data.get('cv'):
            serializer = ApplicantCvUpdateSerializer(data={"cv": data.get('cv')})
            serializer.is_valid(raise_exception=True)
            serializer.update(instance=applicant, validated_data=request.data)
        return super().partial_update(request, *args, **kwargs)

    @action(methods=['post'], detail=False, url_path="export", url_name="export_applicants", )
    def export_applicants(self, request, *args, **kwargs):
        company = Company.objects.filter(pk=request.user.active_company).first()
        applicant = Applicant.objects.filter(pk__in=request.data.get('id_list')) \
            .values("company__name", "position_applied__name", "first_name", "last_name", "email", "phone", "gender",
                    "country", "dob", "level", "skill", "comment", "status", )

        if not applicant:
            return Response({"message": "Applicants not found."}, status=status.HTTP_400_BAD_REQUEST)

        dataframe = pd.DataFrame(list(applicant))
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=f"{company.name}_applicants.csv"'
        dataframe.to_csv(response, encoding='utf-8', header=["Company", "Position Applied", "First Name", "Last Name",
                                                             "Email", "Phone", "Gender", "Country", "Date of Borth",
                                                             "Level", "Skills", "Comment", "Status"])
        return response
