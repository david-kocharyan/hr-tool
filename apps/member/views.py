import uuid
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, status, generics, views
from rest_framework.response import Response

from apps.company.models import Company
from apps.users.models import User

from apps.member.serializers import (MemberSerializer, InviteSerializer, InviteActionSerializer)
from utils.mail_sender import invite_message


class MemberListView(generics.ListAPIView, generics.DestroyAPIView):
    serializer_class = MemberSerializer
    queryset = User.objects.all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['first_name', 'last_name', 'email', ]
    ordering_fields = ['dob', 'email', 'first_name', 'last_name']
    filter_fields = ['dob', 'email', 'first_name', 'last_name']

    def get_queryset(self):
        current_user = self.request.user
        company = Company.objects.filter(pk=current_user.active_company).first()
        return company.members.all()

    def destroy(self, request, *args, **kwargs):
        company = Company.objects.filter(pk=request.user.active_company).first()
        user = company.members.filter(pk=kwargs.get('id')).first()
        if not user:
            return Response({"message": "User not found. Please enter correct ID."}, status=status.HTTP_404_NOT_FOUND)

        company.members.remove(user.pk)
        return Response({"message": "User has been removed from company successfully."},
                        status=status.HTTP_204_NO_CONTENT)


class InviteView(views.APIView):
    serializer_class = InviteSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)

        company = Company.objects.filter(pk=request.user.active_company).first()
        invite_token = uuid.uuid4()
        invite = serializer.create_invitation(serializer.validated_data, company, invite_token)

        if invite:
            invite_message(serializer.validated_data['email'], company, invite.uuid)

        return Response({"message": "Invitation has been send successfully."}, status=status.HTTP_200_OK)


class InviteActionView(views.APIView):
    serializer_class = InviteActionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)

        company = Company.objects.filter(pk=request.user.active_company).first()
        invite_token = uuid.uuid4()
        invite = serializer.create_invitation(serializer.validated_data, company, invite_token)

        if invite:
            invite_message(serializer.validated_data['email'], company, invite.uuid)

        return Response({"message": "Invitation has been send successfully."}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        print(kwargs)