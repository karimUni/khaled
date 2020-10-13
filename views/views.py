from django.shortcuts import render
from serializers.serializers import (
    Registeration_serializer , Contact_serializer , Features_serializer , Get_user_serializer , News_serializer , Update_news_serializer ,Get_all_news
)
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.http import HttpResponse
from .login import LoginSerializer
from config.decorators import admin_role , editor_role
from django.contrib.auth import get_user_model
from models.models import News, Contact , Features
from config.permissions import base64_file
from django.shortcuts import get_object_or_404
# import base64
# from django.core.files.base import ContentFile

# Create your views here.
"""
    add new user to admin panel for website this is the role for admin only that can add users 
    so he can do that by add the following fields =[username , email , role , password , confirm_password]
"""
@api_view(['POST'])
@admin_role
def registeration_view(request):
    User = get_user_model()
    email = request.data.get("email")
    username = request.data.get("username")
    if User.objects.filter(email=email).exists():
        return Response({"detail": "this email is already registered"}, 403)
    elif User.objects.filter(username=username).exists():
        return Response({"detail": "this username is already registered"}, 403)
    else:
        serializer = Registeration_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"successfully created a new user."},200)
        else:
            return Response(serializer.errors,403)

"""
    get all users for website this is the role for admin only that can show all users data
    in accademic affaires website
"""
@api_view(['GET'])
@admin_role
def get_all_users(request):
    User = get_user_model()
    user  = request.user
    username = user.username
    all_users = User.objects.exclude(username=username).exclude(is_superuser=True)
    serializer = Get_user_serializer(instance=all_users,many=True)
    return Response(serializer.data,200)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        new_serializer = serializer.login()
        return Response(new_serializer,200)
    else:
        return Response(serializer.errors,403)

"""
    add new contact this is function for all users to send feedback on our website to share with us there suggestions
    the fields = [name , email ,  subject is not required , message]
"""
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def add_contact(request):
    serializer = Contact_serializer(data=request.data)
    if serializer.is_valid():
        new_serializer = serializer.save()
        return Response({"success":"your feedback has send successfully"},200)
    else:
        return Response(serializer.errors,403)

"""
    list and display all contact and feedback that is the admin role has able to see all data
    and see his suggestion and feedback
"""
@api_view(['GET'])
@admin_role
def get_all_contacts(request):
    all_contacts = Contact.objects.all()
    serializer = Contact_serializer(instance=all_contacts , many=True)
    return Response(serializer.data,200)

"""
    the user can select a feature from our features in the application so any user can do that and send for us the fields
    [name , email ,  select a feature and send to us a message or feedback]
"""

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def select_feature(request):
    serializer = Features_serializer(data=request.data)
    if serializer.is_valid():
        new_serializer = serializer.save()
        return Response({"data":serializer.data},200)
    else:
        return Response(serializer.errors,403)


"""
    the new api its a function to add a new in the website to show in public for all users
    and this is call the serializer that named = News_serializer and this is a role for both 
    admin and editor
"""
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_news(request):
    user = request.user
    serializer = News_serializer(data=request.data)
    # print(base64_file(request.data['str_image']))
    if serializer.is_valid():
        new_serializer = serializer.save(author=user.username)
        return Response({"data":serializer.data},200)
    else:
        return Response(serializer.errors,403)

@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
def get_news(request):
    try:
        news = News.objects.all()
        serializer = Get_all_news(instance=news,many=True)
        return Response(serializer.data,200)
    except News.DoesNotExist:
        return Response({"detail":"there is news yet"},403)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_news(request,news_id):
    user = request.user
    news = get_object_or_404(News,id=int(news_id))
    img = news.news_image
    if "str_image" in request.data:
        img= base64_file(request.data['str_image'])
    serializer = Update_news_serializer(data=request.data ,instance=news)
    if serializer.is_valid():
        new_item = serializer.save(author=user,news_image=img)
        # if "str_image" in request.data:
        #     new_serializer.news_image= base64_file(request.data['str_image'])
        # new_serializer.save()
        return Response({"success":"news updated successfully"},200)
    else:
        return Response(serializer.errors,403)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_news(request,news_id):
    user = request.user
    news = get_object_or_404(News,id=int(news_id))
    news.delete()
    return Response({"success":"news deleted successfully"},200)
    