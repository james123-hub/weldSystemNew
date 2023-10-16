import os
from PIL import Image, ImageEnhance, ImageFilter
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm, ImageUploadForm, ImageForm
from django.contrib import messages
from django.urls import reverse

from .utils import handle_uploaded_image


def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        # 保存原始图片
        with open(os.path.join('media', 'pics', image.name), 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        # 进行图片处理
        processed_image = process_image(image,request)

        # 保存处理后的图片
        processed_image_path = os.path.join('media', 'result', image.name)
        processed_image.save(processed_image_path)

        image_path = os.path.join('media', 'pics', image.name)
        context = {
            'processed_image_path': processed_image_path,
            'image_path': image_path
        }
        return render(request, 'result.html', context)

    return render(request, 'upload.html')

def process_image(image,request):
    # 读取图片
    img = Image.open(image)
    contrast = float(request.POST.get('contrast'))
    saturation = float(request.POST.get('saturation'))
    brightness = int(request.POST.get('brightness'))
    gaussian = float(request.POST.get('gaussian'))

    # 修改对比度
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast)

    # 修改饱和度
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(saturation)

    # 修改亮度
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(brightness / 100.0)

    # 高斯滤波
    img = img.filter(ImageFilter.GaussianBlur(gaussian))

    # 返回处理后的图片对象
    return img

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('upload_image')
        else:
            messages.error(request, '用户名或密码错误')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # 注册成功后，重定向到登录页面
            redirect_url = reverse('login')
            messages.success(request, '注册成功！请等待管理员批准。')
            return redirect(redirect_url)
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


# def image_upload(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             image = form.cleaned_data['image']
#             handle_uploaded_image(image)
#             uploaded_image_url = os.path.join(settings.MEDIA_URL, 'pic/' + image.name)
#             return render(request, 'image_upload.html', {'form': form, 'uploaded_image_url': uploaded_image_url})
#     else:
#         form = ImageUploadForm()
#
#     return render(request, 'image_upload.html', {'form': form, 'uploaded_image_url': None})
#
# def save_image(request):
#     if request.method == 'POST':
#         image_url = request.POST['image']
#         image_name = os.path.basename(image_url)
#         adjusted_image_path = os.path.join(settings.MEDIA_ROOT, 'result/', image_name)
#
#         img = Image.open(os.path.join(settings.BASE_DIR, image_url))
#
#         # 保存调整亮度后的图片
#         brightness = 0
#         enhancer = ImageEnhance.Brightness(img)
#         adjusted_img = enhancer.enhance(1 + brightness / 100)
#         adjusted_img.save(adjusted_image_path)
#
#         return HttpResponse("Image saved successfully.")
#     return HttpResponse("Invalid request.")
# def upload_image(request):
#     if request.method == 'POST':
#         form = ImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             image = form.cleaned_data['image']
#             image_obj = Image(image=image)
#             image_obj.save()
#             return redirect('process_image', image_id=image_obj.id)
#     else:
#         form = ImageForm()
#     return render(request, 'image_upload.html', {'form': form})
#
# def process_image(request, image_id):
#     try:
#         image = Image.objects.get(id=image_id)
#     except Image.DoesNotExist:
#         return redirect('upload_image')
#
#     return render(request, 'process.html', {'image': image})