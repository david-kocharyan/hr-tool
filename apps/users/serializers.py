from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, ForgetPassword


class TokenObtainPairPatchedSerializer(TokenObtainSerializer):

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        user = User.objects.filter(email=attrs['email']).first()
        if not user:
            raise serializers.ValidationError({'email': 'There is no user with this credentials'})

        if not user.password:
            raise serializers.ValidationError({'password': 'Please verify user and set password'})

        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['user'] = UserSerializer(self.user).data
        data['token'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'dob',
            'is_active',
            'auth_provider',
            'active_company',
        )
        extra_kwargs = {'password': {'write_only': True}}
        depth = 1


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(max_length=125)
    password_confirm = serializers.CharField(max_length=125)
    first_name = serializers.CharField(max_length=125)
    last_name = serializers.CharField(max_length=125)
    dob = serializers.DateField()

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'dob',
            'password',
            'password_confirm',
        )

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({'password': 'Password should be match to Password Confirm.'})
        return attrs

    def validate_password(self, value):
        """Validates that a password is as least 8 characters long and has at least 2 digits and 1 Upper case letter."""
        value = str(value)
        if len(value) < 6:
            raise serializers.ValidationError('Password must be at least 6 characters long.')

        if sum(c.isdigit() for c in value) < 2:
            raise serializers.ValidationError('Password must container at least 2 digits.')

        if not any(c.isupper() for c in value):
            raise serializers.ValidationError('Password must container at least 1 uppercase letter.')

        return value

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            dob=validated_data['dob'],
            is_active=True,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=False)
    new_password = serializers.CharField(required=False)
    new_password_confirm = serializers.CharField(required=False)

    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('new_password_confirm'):
            raise serializers.ValidationError({'password': 'Password should be match to Password confirm.'})
        return attrs

    def validate_old_password(self, value):
        if not self.instance.check_password(value):
            raise serializers.ValidationError({'password': 'Old password is incorrect. Please enter right password.'})

    def validate_new_password(self, value):
        """Validates that a password is as least 8 characters long and has at least 2 digits and 1 Upper case letter."""
        value = str(value)
        if len(value) < 6:
            raise serializers.ValidationError('Password must be at least 6 characters long.')

        if sum(c.isdigit() for c in value) < 2:
            raise serializers.ValidationError('Password must container at least 2 digits.')

        if not any(c.isupper() for c in value):
            raise serializers.ValidationError('Password must container at least 1 uppercase letter.')

        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError('User not found. Please enter correct email.')
        if user.auth_provider != "email":
            raise serializers.ValidationError(f"You don't have password. Please continue with {user.auth_provider}")

        verify = ForgetPassword.objects.filter(user=user).first()
        if verify:
            raise serializers.ValidationError("We have sent a link to your email address.")

        return value

    def create_verification_link(self, validated_data, code):
        user = User.objects.filter(email=validated_data['email']).first()
        verification = ForgetPassword.objects.create(user=user, uuid=code)
        data = {
            'user': user,
            'verification': verification,
        }
        return data


class SetForgetPasswordSerializer(serializers.Serializer):
    id = serializers.IntegerField(write_only=True)
    password = serializers.CharField(max_length=125)
    password_confirm = serializers.CharField(max_length=125)

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({'password': 'Password should be match to Password Confirm.'})
        return attrs

    def validate_password(self, value):
        """Validates that a password is as least 8 characters long and has at least 2 digits and 1 Upper case letter."""
        value = str(value)
        if len(value) < 6:
            raise serializers.ValidationError('Password must be at least 6 characters long.')

        if sum(c.isdigit() for c in value) < 2:
            raise serializers.ValidationError('Password must container at least 2 digits.')

        if not any(c.isupper() for c in value):
            raise serializers.ValidationError('Password must container at least 1 uppercase letter.')

        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        ForgetPassword.objects.filter(user=instance).delete()
        return instance
