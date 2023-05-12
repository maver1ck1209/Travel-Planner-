from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('home', views.index, name="home"),
    path('login', views.login_user, name = "login"),
    path('sign-up', views.signup, name = "signup"),
    path('pyt', views.pyt, name = "pyt"),
]