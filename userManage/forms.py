from django import forms
from django.core.exceptions import ValidationError


class UserRegForm(forms.Form):
    userName = forms.CharField(max_length = 30 , error_messages={'required': '用户姓名不能为空', 'max_length': '用户名长度不超过30位'})
    pwd = forms.CharField(max_length = 20 , error_messages={'required': '密码不能为空', 'max_length': '密码长度不超过20位'})
    pwdcf = forms.CharField(max_length = 20 , error_messages={'required': '密码不能为空', 'max_length': '密码长度不超过20位'})

    def clean(self):
        pwd = self.cleaned_data.get("pwd")
        pwdcf = self.cleaned_data.get("pwdcf")
        if pwd != pwdcf:
            self.add_error("re_password", ValidationError("两次密码不一致"))