import wtforms
from wtforms import FileField
from wtforms.validators import length, email, EqualTo
from models import EmailCaptchaModel, UserModel
from flask_wtf.file import FileField, FileAllowed, FileRequired


# 登录表单验证
class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])


class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3, max=20)])
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])
    password = wtforms.StringField(validators=[length(min=6, max=20)])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            raise wtforms.ValidationError("邮箱验证码错误！")

    def validate_email(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            raise wtforms.ValidationError("邮箱已经存在！")


# 个人资料验证
class UserInfoFrom(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3, max=20)])
    phone = wtforms.StringField(validators=[length(min=11, max=11)])
    address = wtforms.StringField(validators=[length(max=20)])
    signature = wtforms.StringField(validators=[length(max=200)])
    introduction = wtforms.StringField(validators=[length(max=200)])


# 修改密码设置
class UserSettingForm(wtforms.Form):
    oldPassword = wtforms.StringField(validators=[length(min=6, max=20)])
    newPassword = wtforms.StringField(validators=[length(min=6, max=20)])
    newPassword_confirm = wtforms.StringField(validators=[EqualTo("newPassword")])


# 发表菜品
class PostRecipeForm(wtforms.Form):
    recipe_name = wtforms.StringField(validators=[length(min=1)])
    recipe_introduction = wtforms.StringField(validators=[length(min=1,)])
    recipe_steps = wtforms.StringField(validators=[length(min=1)])
    avatar = FileField('image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])


# 删除菜品记录
class DeleteRecipeForm(wtforms.Form):
    recipe_id = wtforms.StringField(validators=[length(min=1, max=20)])


# 个人头像
class UserAvatarForm(wtforms.Form):
    avatar = FileField('image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])


# 修改菜品
class EditRecipeForm(wtforms.Form):
    recipe_id = wtforms.StringField(validators=[length(min=1, max=20)])
    recipe_name = wtforms.StringField()
    recipe_introduction = wtforms.StringField()
    recipe_steps = wtforms.StringField()
    avatar = FileField('image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])


class CommentForm(wtforms.Form):
    content = wtforms.StringField(validators=[length(min=1)])
