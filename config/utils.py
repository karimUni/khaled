import datetime
import jwt
from django.conf import settings
from rest_framework.authtoken.models import Token


def generate_access_token(user):
    #hours=8,minutes=30
    access_token_payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8,minutes=30),
        "iat": datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(
        access_token_payload, settings.SECRET_KEY, algorithm="HS256"
    ).decode("utf-8")
    return access_token


def generate_refresh_token(user, token_version):
    refresh_token_payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
        "iat": datetime.datetime.utcnow(),
        "token": token_version,
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.REFRESH_TOKEN_SECRET, algorithm="HS256"
    ).decode("utf-8")

    return refresh_token
