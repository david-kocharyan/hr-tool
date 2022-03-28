import uuid
from datetime import datetime
from rest_framework.exceptions import AuthenticationFailed
from apps.users.models import User


def register_social_user(data):
    email = data.get('email')
    filtered_user_by_email = User.objects.filter(email=email).first()

    if filtered_user_by_email:
        if data.get('provider') == filtered_user_by_email.auth_provider:
            return {"user": filtered_user_by_email, 'token': filtered_user_by_email.tokens()}
        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email.auth_provider
            )
    else:
        user = {
            'email': data.get('email'),
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'dob': datetime.strptime(data.get('dob'), "%m/%d/%Y").strftime("%Y-%m-%d") if data.get('dob') else None,
        }

        user = User.objects.create(**user)
        user.set_password(str(uuid.uuid1()))
        user.is_active = True
        user.auth_provider = data.get('provider')
        user.save()

        return {'user': user, 'token': user.tokens()}
