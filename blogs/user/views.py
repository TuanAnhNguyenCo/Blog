from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect


def Login(request):
    # Đã đăng nhập rồi thì đưa vào home
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('post:home'))
    # Đưa ra trang login
    if request.method == 'GET':
        return render(request,'user/login.html')

    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(email = email,password = password)
    # Đăng nhập
    if user != None:
        login(request,user)
        return HttpResponseRedirect(reverse('post:home'))
    else:
         return render(request,'user/login.html')

def Logout(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('post:home'))
    logout(request)
    return HttpResponseRedirect(reverse('post:home'))

def Register(request):
    return render(request,'user/register.html')



    