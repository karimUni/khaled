from django.contrib import admin
from django.contrib.auth import get_user_model 
from models.models import News , Contact ,Features ,DigitsSecurity
from rest_framework.authtoken.models import Token
# Register your models here.

User = get_user_model()
# admin.site.register(User,UserAdmin)
# admin.site.register(Token)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email','role')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    pass

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass

@admin.register(Features)
class FeaturesAdmin(admin.ModelAdmin):
    pass

@admin.register(DigitsSecurity)
class DigitsSecurityAdmin(admin.ModelAdmin):
    pass

