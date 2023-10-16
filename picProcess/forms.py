from django import forms
from .models import Image
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ImageForm(forms.Form):
    image = forms.ImageField()
class ImageUploadForm(forms.Form):
    image = forms.ImageField()
class RegistrationForm(UserCreationForm):
    USER_CHOICES = (
        ('ordinary', '普通用户'),
        ('admin', '管理员'),
    )
    user_type = forms.ChoiceField(label='用户类型', choices=USER_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'user_type')