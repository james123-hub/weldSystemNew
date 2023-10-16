import PIL.ImageEnhance
from django.conf import settings
import os


def handle_uploaded_image(image):
    img = PIL.Image.open(image)

    # 调整图片亮度
    brightness = 0
    enhancer = PIL.ImageEnhance.Brightness(img)
    img = enhancer.enhance(1 + brightness / 100)

    # 保存图片
    pic_path = os.path.join(settings.MEDIA_ROOT, 'pic')
    if not os.path.exists(pic_path):
        os.makedirs(pic_path)
    img.save(os.path.join(pic_path, image.name))
