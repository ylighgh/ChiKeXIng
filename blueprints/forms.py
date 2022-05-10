import wtforms
from wtforms.validators import length, email, EqualTo
from models import User_setting


# 登录表单验证
class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])
