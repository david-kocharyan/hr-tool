from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from .serializers import FacebookSocialAuthSerializer, GoogleSocialAuthSerializer


class FacebookSocialAuthView(GenericAPIView):
    serializer_class = FacebookSocialAuthSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        """
        POST with "auth_token"
        Send an access token as from facebook to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data['auth_token'])
        return Response(data, status=status.HTTP_200_OK)


class GoogleSocialAuthView(GenericAPIView):
    serializer_class = GoogleSocialAuthSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data['auth_token'])
        return Response(data, status=status.HTTP_200_OK)
