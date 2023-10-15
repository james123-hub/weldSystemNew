import os
from PIL import Image, ImageEnhance, ImageFilter
from django.shortcuts import render
from django.http import HttpResponse

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
