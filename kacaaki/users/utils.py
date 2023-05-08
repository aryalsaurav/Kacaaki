import datetime

import pytz
from django.utils import timezone
from django.core.mail import send_mail


def custom_create_token(token_model, user, serializer):
    token = token_model.objects.create(user=user)
    utc_now = timezone.now()
    utc_now = utc_now.replace(tzinfo=pytz.utc)
    token.created = utc_now
    token.save()
    return token



def user_verification_email(user):
    send_mail(
        "Verify your email",
        "Please verify your email by clicking the link below: "
        "http://127.0.0.1:8000/api/user/verify-email/{}".format("hello") ,
        "noreply@gmail.com",
        [user.email],
        fail_silently=False,
    )