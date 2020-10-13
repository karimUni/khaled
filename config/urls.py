from django.urls import path
from views import views as controller
from django.conf.urls import url
from config.sendMail import send_email , recieve_email
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('add_user/',controller.registeration_view),
    path('get_users/',controller.get_all_users),
    path('login/',controller.login,name='login'),
    path('send_email/',send_email),
    path('set_password/',recieve_email),
    path('add_news/',controller.add_news),
    path('get_news/',controller.get_news),
    path('edit_news/<int:news_id>/',controller.edit_news),
    path('delete_news/<int:news_id>/',controller.delete_news),
    path('send_feedback/',controller.add_contact),
    path('select_feature/',controller.select_feature),
    path('get_contacts/',controller.get_all_contacts)
    # url(r'^image/example.png$',controller.show_image)
    # path('image/',controller.show_image)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)