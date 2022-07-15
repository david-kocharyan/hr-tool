import datetime

from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def forget_password_message(user, verification):
    context = {
        'email': user.email,
        'full_name': f'{user.first_name} {user.last_name}',
        'link_url': f'{settings.FRONTEND_URL}/forget-password-verification/{verification.uuid}/',
        'image': f'{settings.BASE_URL}/static/img/email_logo.png',
        'year': datetime.datetime.now().year
    }

    msg_html = render_to_string('mails/forget_password.html', context)
    recipient_list = [user.email]

    return send_mail('Forget password request', '', settings.DEFAULT_FROM_EMAIL, recipient_list, html_message=msg_html)


def invite_message(email, company, invite_token):
    context = {
        'email': email,
        'company': company,
        'link_url': f'{settings.FRONTEND_URL}/members-invite/{invite_token}/',
        'image': f'{settings.BASE_URL}/static/img/email_logo.png',
        'year': datetime.datetime.now().year
    }

    msg_html = render_to_string('mails/member_invitation.html', context)
    recipient_list = [email]

    return send_mail(f"Invite to {company}", '', settings.DEFAULT_FROM_EMAIL, recipient_list, html_message=msg_html)
