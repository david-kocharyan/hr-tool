import os
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from . import facebook, google
from .register import register_social_user
from ..users.serializers import UserSerializer


class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)
        try:
            if not user_data.get('email'):
                raise serializers.ValidationError('Invalid email address. Please login again.')

            data = {
                'user_id': user_data.get('id'),
                'email': user_data.get('email'),
                'first_name': user_data.get('first_name'),
                'last_name': user_data.get('last_name'),
                'dob': user_data.get('birthday'),
                'provider': 'facebook'
            }
            user_data = register_social_user(data=data)

            return {'user': UserSerializer(instance=user_data.get('user')).data, 'token': user_data.get('token')}

        except Exception as identifier:
            raise serializers.ValidationError(
                'The token is invalid or you have already registered. Please login again.')


class GoogleSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of google related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            if user_data['aud'] != os.environ.get('GOOGLE_CLIENT_ID'):
                serializers.ValidationError('The token is invalid or expired. Please login again.')
            if not user_data.get('email'):
                raise serializers.ValidationError('Invalid email address. Please login again.')

            data = {
                'user_id': user_data.get('sub'),
                'email': user_data.get('email'),
                'first_name': user_data.get('given_name'),
                'last_name': user_data.get('family_name'),
                'dob': user_data.get('birthday'),
                'provider': 'google'
            }
            user_data = register_social_user(data=data)

            return {'user': UserSerializer(instance=user_data.get('user')).data, 'token': user_data.get('token')}

        except Exception as identifier:
            raise serializers.ValidationError('The token is invalid or expired. Please login again.')
