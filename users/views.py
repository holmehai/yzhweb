#-*-coding:utf-8-*-
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse

from  .models import UserProfile , EmailVerifyRecord , Message
from .forms import LoginForm , RegisterForm , ForgetpwdForm , ModifypwdForm , MessageForm
from utils.email_send import send_register_email



# Create your views here.
# 允许使用邮箱为登录名


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            #并集查询？
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self,request):
        return render(request, 'login.html', {})
    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, 'login.html', {"msg": u"此账号未激活"})
            else:
                return render(request,'login.html',{"msg": u"用户名或密码错误"})
        else:
            return render(request, 'login.html', {"login_form":login_form})



class LogoutView(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))

class RegisterView(View):
    def get(self,request):
        register_form =RegisterForm()
        return render(request,'register.html',{'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form': register_form,'msg':u'用户已存在'})
            pass_word = request.POST.get("password", "")
            user_profile= UserProfile()
            user_profile.username =user_name
            user_profile.password = make_password(pass_word)
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.save()

            send_register_email(user_name,'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html',{'register_form':register_form})


class ActiveUserView(View):
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
             return render(request, 'active_fail.html')#验证失败的返回


        return render(request, 'login.html')



class ForgetpwdView(View):
    def get(self,request):
        forgetpwd_form = ForgetpwdForm()
        return render(request,'forgetpwd.html',{'forgetpwd_form':forgetpwd_form})

    def post(self,request):
        forgetpwd_form = ForgetpwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get('email','')
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form})


class ResetView(View):
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html',{'email':email})
        else:
            return render(request, 'active_fail.html')
        return render(request,'login.html')


class ModifypwdView(View):
    def post(self,request):
        modify_form = ModifypwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password1', '')
            email =request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email,'msg':u'密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html')

        else:
            email = request.POST.get('email','')
            return render(request, 'password_reset.html', {'email': email,'modify_form':modify_form})


class MessageView(View):
    def get(self,request):
        return render(request, 'index.html',{})
    def post(self,request):
        message_form = MessageForm(request.POST)
        # if message_form.is_valid():
        name = request.POST.get('contact_name', '')
        email = request.POST.get('contact_email', '')
        message = request.POST.get('contact_message', '')
        contact_message = Message()
        contact_message.name = name
        contact_message.email = email
        contact_message.message = message
        contact_message.save()
        return render(request, "message_success.html")
        # else:
        #     return render(request, "index.html")
