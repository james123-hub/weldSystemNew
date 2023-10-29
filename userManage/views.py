from django.http import HttpResponse
from django.shortcuts import render
from .forms import UserRegForm
from .models import userInfo


# Create your views here.
def login(request):
    return render(request, 'user_login.html')
def register(request):
    if request.method == "GET":
        return render(request, 'user_reg.html')
    if request.method == "POST":
        form_obj = UserRegForm(request.POST)
        if form_obj.is_valid():
            username = request.POST.get("userName")
            password = request.POST.get("pwd")
            if userInfo.objects.filter(username = username):
                info = '用户名已存在'
                return render(request, 'user_reg.html', {"info": info})
            user = userInfo()
            user.username = username
            user.password = password
            user.status = '0'
            user.save()
            return render(request, 'user_reg.html', {"success": '用户注册成功'})
        else:
            errors = form_obj.errors
            return render(request, 'user_reg.html', {"errors": errors})
    return render(request, 'user_reg.html')