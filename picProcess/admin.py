from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Image

class imageAdmin(admin.ModelAdmin):
    list_display = ["photo"]

admin.site.register(Image, imageAdmin)
