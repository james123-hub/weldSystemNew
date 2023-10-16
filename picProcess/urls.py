from django.urls import path
from .import views

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    # path('save/', views.save_image, name='save_image'),
    path('register/', views.register, name='register'),
    path('', views.user_login, name='login'),
    # path('process/<int:image_id>/', views.process_image, name='process_image'),
]