from django.urls import path
from .import views

urlpatterns = [
    path('',views.homepage, name='homepage'),
    path('result/', views.index, name='index'),
    path('upload/', views.uploadView, name='upload_image'),
    path('process/', views.process_image, name='process_image')
]