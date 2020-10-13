import re
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import get_user_model
import jwt
from django.conf import settings
from rest_framework import exceptions
from django.shortcuts import get_object_or_404
import base64
from django.core.files.base import ContentFile
from django.conf import settings
import uuid
import os

def validate_password(password):
    pattern = '[A-Z]+[a-z]$'
    if len(password) < 8:
        return "Make sure your password is at least 8 letters"
    elif re.search('[0-9]',password) is None:
        return "Make sure your password has a number in it"
    elif re.search('[a-z]',password) is None: 
        return "Make sure your password has a letters in it"
    return "success"


class Base_authentiction(BaseAuthentication):
    def authenticate(self,request):
        User = get_user_model()
        headers = request.headers.get('Authorization')
        if not headers:
            return None
        try:
            access_token = headers.split(" ")[1]
            payload = jwt.decode(access_token,settings.SECRET_KEY,algorithm=["HS256"])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("access token expired")
        except IndexError:
            raise exceptions.AuthenticationFailed("wrong access token")
        except Exception as e:
            raise exceptions.AuthenticationFailed(e)

        active_user = get_object_or_404(User,id=payload["user_id"])
        return (active_user,None)


# def base64_file(data):
#     if 'data:' in data and ';base64,' in data:
#         path = settings.MEDIA_ROOT + '/news/'
#         # path = "E:\\unilearn\\Accademic affaire\\accademicaffairs\\media\\news\\"
#         _format, _img_str = data.split(';base64,')
#         _name, ext = _format.split('/')
#         # print(_name)
#         # if not _name:
#         name = _name.split(":")[-1]
#         file_name = str(uuid.uuid4())[:12]
#         complete_file_name = "%s.%s" % (file_name, ext,)
#         try:
#             full_path = path + complete_file_name
#             with open(full_path,'wb') as img:
#                 img.write(base64.b64decode(_img_str))
#                 img.close()
#             return full_path
#         except Exception as e:
#             raise exceptions.ValidationError('Invalid image data')

def base64_file(data):
    if 'data:' in data and ';base64,' in data:
        news_path = os.path.join(os.path.join(settings.BASE_DIR, 'media'), 'news')
        _format, _img_str = data.split(';base64,')
        _name, ext = _format.split('/')
        file_name = str(uuid.uuid4())[:12]
        complete_file_name = "%s.%s" % (file_name, ext,)
        try:
            with open(f'{news_path}/{complete_file_name}', 'wb') as img:
                img.write(base64.b64decode(_img_str))
                return f'{news_path}/{complete_file_name}'
        except Exception as e:
            raise exceptions.ValidationError(f'{e}. Invalid image data')