import os

from PIL import ImageEnhance, ImageFilter
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from .forms import ImageUploadForm
from django.http import JsonResponse
import base64
from io import BytesIO
from django.conf import settings
from PIL import Image

# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')
def index(request):
    data = Image.objects.all()
    context = {
        'data' : data
    }
    return render(request,"display.html", context)
def uploadView(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
            form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})
def process_image(request):
    if request.method == 'POST':
        contrast = float(request.POST.get('contrast'))
        saturation = float(request.POST.get('saturation'))
        brightness = int(request.POST.get('brightness'))
        gaussian = float(request.POST.get('gaussian'))



        # 加载原始图片
        img = Image.open('F:\weldSystem\media\pics\mAP.png')

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

        # 转换为Base64编码并返回
        img_base64 = img_to_base64(img)
        return JsonResponse({'image': img_base64})

    return render(request, 'process_image.html')
def img_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="png")
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"
# def process_image(request):
#     if request.method == 'POST':
#         image = request.FILES['image']
#
#         # 保存原始图片
#         original_image_name = image.name
#         original_image_path = os.path.join(settings.MEDIA_ROOT, 'original_images', original_image_name)
#         with open(original_image_path, 'wb') as f:
#             for chunk in image.chunks():
#                 f.write(chunk)
#
#         # 处理图片
#         img = Image.open(original_image_path)
#         img_dir, img_filename = os.path.split(original_image_path)
#         processed_image_path = os.path.join(img_dir, 'processed_images',  img_filename)
#         img = img.point(lambda p: p * float(request.POST['contrast']))
#         img.save(processed_image_path)
#
#         # 返回原始图片路径和处理后图片路径
#         return JsonResponse({
#             'original_path': settings.MEDIA_URL + 'original_images/' + original_image_name,
#             'processed_path': settings.MEDIA_URL + 'original_images/processed_images/processed_' + img_filename,
#         })
#
#     return render(request, 'process_image1.html')


