from django import forms

class LoginForm(forms.Form):
    login_username = forms.CharField(
        required=True, 
        error_messages={
            "required": "输入错误——用户名不能为空！",
            "invalid": "输入错误——用户名格式错误！",
        }
    )

    login_password = forms.CharField(
        label="密码",
        min_length=6,
        error_messages={
            "required": "输入错误——密码不能为空",
            'min_length':'输入错误——密码不能少于6位',
        },
        widget=forms.widgets.PasswordInput(
            attrs={'class': 'form-control'},  # 给生成的标签添加属性
            render_value=True  # 返回报错信息的时候要不要展示密码
        )
    )

    email = forms.EmailField(
        required=True,
        error_messages={
            'invalid':"邮箱格式不正确"
        }
    )

class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=200)

    file = forms.FileField()
    print(file)