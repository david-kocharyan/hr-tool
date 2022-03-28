import uuid
from django.db import transaction
from rest_framework import views, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.token_blacklist.models import (OutstandingToken, BlacklistedToken)

from apps.users.models import User, ForgetPassword
from apps.users.serializers import (TokenObtainPairPatchedSerializer, UserRegistrationSerializer, UserSerializer,
                                    ChangePasswordSerializer, ForgetPasswordSerializer, SetForgetPasswordSerializer, )

from utils.mail_sender import forget_password_message


class UserRegisterView(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.create(serializer.validated_data)

        refresh = RefreshToken.for_user(new_user)

        return Response({'user': UserSerializer(instance=new_user).data,
                         'token': {
                             'refresh': str(refresh),
                             'access': str(refresh.access_token),
                         }}, status=status.HTTP_200_OK)


class TokenObtainPairPatchedView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = TokenObtainPairPatchedSerializer


class UserLogoutView(views.APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': "User logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as err:
            return Response({'message': 'Something went wrong, please try again.'}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutAllView(views.APIView):
    def post(self, request):
        try:
            tokens = OutstandingToken.objects.filter(user_id=request.user.id)
            for token in tokens:
                t, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({'message': "User logged out successfully from all devices."},
                            status=status.HTTP_205_RESET_CONTENT)
        except Exception as err:
            return Response({'message': 'Something went wrong, please try again.'},
                            status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer

    def partial_update(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=request.user, validated_data=serializer.validated_data)
        return Response({"message": "Your password has been changed successfully."}, status=status.HTTP_200_OK)


class ForgetPasswordView(views.APIView):
    permission_classes = [AllowAny, ]
    serializer_class = ForgetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.create_verification_link(validated_data=serializer.validated_data, code=uuid.uuid1())
        forget_password_message(data.get('user'), data.get('verification'))

        return Response({'message': "Please check your email. We send verification link."}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        uuid_instance = ForgetPassword.objects.filter(uuid=kwargs.get('uuid')).first()
        if not uuid_instance:
            return Response({'message': 'Forget password verification key is incorrect.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(pk=uuid_instance.user_id).first()
        data = {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}
        return Response({'user': data}, status=status.HTTP_200_OK)


class SetForgetPasswordView(generics.UpdateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = SetForgetPasswordSerializer

    def partial_update(self, request, *args, **kwargs):
        serializer = SetForgetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        verified_user = User.objects.get(pk=serializer.validated_data['id'])
        if not verified_user:
            return Response({'user': "User not found."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.update(instance=verified_user, validated_data=serializer.validated_data)
        return Response({'message': 'Yor password has been change successfully.'}, status=status.HTTP_200_OK)
