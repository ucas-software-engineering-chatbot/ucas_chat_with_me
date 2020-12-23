from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('login', views.login),
    path('index', views.index),

    path('chat', views.chat),
    path('beautiful', views.beautiful),
    path('management', views.management),
    path('management_email', views.management_email),
]