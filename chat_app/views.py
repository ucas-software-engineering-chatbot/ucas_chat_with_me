import json
import os

from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.contrib import auth #引入auth模块
from django.contrib.auth.models import User # auth应用中引入User类
from django.core.exceptions import ValidationError
from chat_app.forms import LoginForm, UploadFileForm

def login(request):
    if request.method == 'GET':
        print("===> Error")
        return render(request, 'chat_app/login.html')
    else:
        login_form = LoginForm(request.body)
        if login_form.is_valid:
            username = request.POST.get("login_username")
            password = request.POST.get("login_password")
            user_obj = auth.authenticate(username=username, password=password)
            # print("[当前用户状态]" + str(user_obj))
            print(username)
            if user_obj:
                auth.login(request, user_obj)
                print("[当前用户状态]" + str(request.user.is_authenticated))
                return render(request, 'chat_app/index.html')
            else:
                response = {
                    "status": 400,
                    "data": "用户名或者密码错误请重新输入"
                }
                return render(request, 'chat_app/login.html', response)
        else:
            print(login_form)
            response = {
                "status": 400,
                "data": login_form.errors
            }
            return render(request, 'chat_app/login.html', response)

def index(request):
    return render(request, 'chat_app/index.html')

def chat(request):
    return render(request, 'chat_app/chat.html')

def beautiful(request):
    return render(request, 'chat_app/beautiful.html')

def management(request):
    if request.user.is_authenticated:
        username = request.user
        print(request.user)
        response = {
            "status": 200,
            "username": username,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "is_superuser": request.user.is_superuser,
            "email": request.user.email,
        }
        return render(request, 'chat_app/management.html', response)
    else:
        return render(request, 'chat_app/login.html')

def management_email(request):
    if request.method == 'GET':
        return profile(request)
    else:
        change_form = LoginForm(request.body)
        if change_form.is_valid:
            username = request.user
            email = request.POST.get("email")
            user_obj = User.objects.get(username=username)
            if user_obj:
                user_obj.email = email
                user_obj.save()
                request.user.email = email
                return redirect('/chat_app/management', request)
            else:
                response = {
                    "status": 400,
                    "data": "当前用户不存在",
                    "username": username,
                    "email": request.user.email
                }
                return redirect('/chat_app/management', response)
        else:
            response = {
                "status": 400,
                "data": "邮箱格式不正确，请重新输入",
                "username": username,
                "email": request.user.email
            }
            return redirect('/chat_app/management', response)