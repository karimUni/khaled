from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from models.models import DigitsSecurity
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import random
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from config.permissions import validate_password 
from rest_framework.authtoken.models import Token
from config.utils import generate_access_token , generate_refresh_token

@api_view(["POST"])
@permission_classes([AllowAny])
@csrf_exempt
def send_email(request):
    User = get_user_model()
    email = request.data.get("email")

    try:
        user = get_object_or_404(User, email=email)
    except:
        return Response({"detail": "user not found"}, 404)
    new_user = int(user.id)
    digits = [0, 0, 0, 0, 0, 0]
    Secret_digits = ""
    for i in digits:
        Secret_digit = int(random.random() * 10)
        Secret_digits += str(Secret_digit)
    if DigitsSecurity.objects.filter(user=user).exists():
        digit_code = DigitsSecurity.objects.get(user=user)
        digit_code.digits=Secret_digits
        digit_code.save()
    new_Secret_digits = DigitsSecurity(user=user, digits=Secret_digits)
    new_Secret_digits.save()
    send_mail(
        "Contact Form",
        "Your secret key is {}".format(Secret_digits),
        settings.EMAIL_HOST_USER,
        ["{}".format(email)],
        fail_silently=False,
    )

    return Response({"success": "check your email: {}".format(email)}, 201)


@api_view(["POST"])
@permission_classes([AllowAny])
@csrf_exempt
def recieve_email(request):
    User = get_user_model()
    code = request.data.get("code")
    password = request.data.get('password')
    response = Response()
    # if code is None:
    #     return Response({"error": "code not found"}, 404)
    try:
        digits = DigitsSecurity.objects.get(digits=code)
    except:
        return Response({"detail": "code not found"}, 404)
    # digits = DigitsSecurity.objects.get(digits=code)
    if digits is None:
        return Response({"detail": "invalid code"}, 401)
    user_is = digits.user.username
    active_user = User.objects.filter(username=user_is).first()
    if active_user is None:
        return Response({"detail": "user not found"}, 404)
    new_password = validate_password(password)
    if new_password != 'success':
        return Response({"detail":new_password},403)
    active_user.set_password(password)
    active_user.save()
    role = active_user.role
    author = active_user.username

    access_token = generate_access_token(active_user)
    token_version = Token.objects.get(user=active_user).key
    if token_version is None:
        response.data = {"token_version": "token version not exist"}
    refresh_token = generate_refresh_token(active_user, token_version)

    response.data = {
       "access_token": access_token,
        "refresh_token": refresh_token,
        "email": active_user.email,
        "role": active_user.role,
        "author": active_user.username
    }

    return response


def sendEmail(email, username, password):
    try:
        status = send_mail(
            "Contact Form",
            f"you can login in our personal exam system with email: {email}, and password: {password}",
            settings.EMAIL_HOST_USER,
            ["{}".format(email)],
            fail_silently=False,
        )
    except Exception as e:
        "{}".format(e)


# @api_view(["POST"])
# @permission_classes([AllowAny])
# # @ensure_csrf_cookie
# @csrf_exempt
# def test_email(request):
#     email = request.data.get("email")
#     print(email)
#     print(settings.EMAIL_HOST_USER)
#     send_mail(
#         "Contact Form",
#         "test the message has delivered for email {}".format(email),
#         settings.EMAIL_HOST_USER,
#         ["{}".format(email)],
#         fail_silently=False,
#     )
#     return HttpResponse("success sent to email")

