from rest_framework import serializers , exceptions
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from config.utils import *
from rest_framework.authtoken.models import Token

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True , write_only=True)
    
    class Meta:
        fields = ['email','password']

    def check_user(self):
        User = get_user_model()
        email = self.validated_data['email']
        password = self.validated_data['password']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail":"user not found"})
        
        if not user.check_password(password):
            raise serializers.ValidationError({"detail":"wrong password"})
        return user

    def login(self):
        user = self.check_user()
        access_token = generate_access_token(user)
        token_version = get_object_or_404(Token,user=user).key
        refresh_token = generate_refresh_token(user, token_version)
        data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            'email': user.email,
            "role": user.role,
            "author": user.username
        }
        return data
