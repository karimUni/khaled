from rest_framework import serializers
from django.contrib.auth import get_user_model
from config.permissions import validate_password 
from models.models import Contact , Features , News
from django.shortcuts import get_object_or_404
from config.ImageBase64 import Base64ImageField
from config.permissions import base64_file

User = get_user_model()
class Registeration_serializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    class Meta:
        model = User
        fields = ['email','username','role','password','password2']

    def save(self,*args,**kwargs):
        user = User(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
            role = self.validated_data['role']
        )
        if self.validated_data['password'] != self.validated_data['password2']:
            raise serializers.ValidationError({"error":"passwords must matches"})
        password = validate_password(self.validated_data['password'])
        if password != 'success':
            raise serializers.ValidationError({"error":password})
        
        user.set_password(self.validated_data['password'])
        user.save()
        return user

class Get_user_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','username','role']

class Contact_serializer(serializers.ModelSerializer):
    subject = serializers.CharField(required=False ,default=None)
    class Meta:
        model = Contact
        fields = ['id','name','email','subject','message']
        read_only_field = [ "id"]

    def save(self,*args,**kwargs):
        contact = Contact(
            name = self.validated_data['name'],
            email = self.validated_data['email'],
            subject= self.validated_data['subject'],
            message = self.validated_data['message']
        )
        contact.save()
        return contact

class Features_serializer(serializers.ModelSerializer):
    class Meta:
        model = Features
        fields = ['name','email','feature','message']

    def save(self,*args,**kwargs):
        feature = Features(
            name = self.validated_data['name'],
            email = self.validated_data['email'],
            feature= self.validated_data['feature'],
            message = self.validated_data['message']
        )
        feature.save()
        return feature


class News_serializer(serializers.ModelSerializer):
    str_image = serializers.CharField(required=False,allow_null=True)
    class Meta:
        model = News
        fields = ['id','news_author','news_category','news_head','news_body','news_image','str_image']
        read_only_fields = [ 'id','news_author','news_image']

    def save(self,author,*args,**kwargs):
        user = get_object_or_404(User, username=author)
        new = News(
            news_category = self.validated_data['news_category'],
            news_head = self.validated_data['news_head'],
            news_body = self.validated_data['news_body'],
        )
        new.set_news_author(user)
        img =None
        if 'str_image' in self.validated_data and self.validated_data['str_image'] is not None:
            img = base64_file(self.validated_data['str_image'])
        new.set_news_image(img)
        new.save()
        return new

class Update_news_serializer(serializers.ModelSerializer):
    news_category = serializers.CharField(required=False)
    news_head = serializers.CharField(required=False)
    news_body = serializers.CharField(required=False)
    str_image = serializers.CharField(required=False,allow_null=True)
    class Meta:
        model = News
        fields = ['id','news_author','news_category','news_head','news_body','news_image','str_image']
        read_only_fields = [ 'id','news_author','news_image']
    # def save(self,author,*args,**kwargs):
    #     user = get_object_or_404(User, username=author)
    #     new = News(
    #         news_category = self.validated_data['news_category'],
    #         news_head = self.validated_data['news_head'],
    #         news_body = self.validated_data['news_body'],
    #     )
    #     new.set_news_author(user)
    #     img =None
    #     if 'str_image' in self.validated_data and self.validated_data['str_image'] is not None:
    #         img = base64_file(self.validated_data['str_image'])
    #     # new.save()
    #     new.set_news_image(img)
    #     new.save()
    #     return new

class Get_all_news(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id','news_author','news_category','news_head','news_body','news_image']
        # read_only_fields = [ 'id','news_author','news_image']