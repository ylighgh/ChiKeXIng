from datetime import datetime
from flask import Blueprint, render_template, g, request,session, redirect, url_for, flash, jsonify
from flask_mail import Message
from models import EmailCaptchaModel, UserModel
from decorators import login_required
from .forms import UserInfoFrom
import string
import random
from exts import db, mail

# from sqlalchemy import or_

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route('/home')
@login_required
def home():
    return render_template("home.html")


@bp.route('/postRecipe')
@login_required
def postRecipe():
    return render_template("postRecipe.html")


@bp.route('/userRecipe')
@login_required
def userRecipe():
    return render_template("userRecipe.html")


@bp.route('/userInfo', methods=['GET', 'POST'])
@login_required
def userInfo():
    if request.method == 'GET':
        return render_template("userInfo.html")
    else:
        form = UserInfoFrom(request.form)
        if form.validate():
            # 获取当前用户的id值
            user_id = session.get("user_id")
            USER = UserModel.query.filter(UserModel.id == user_id).first()
            USER.username = form.username.data
            USER.email = form.email.data
            USER.phone = form.phone.data
            USER.address = form.address.data
            USER.signature = form.signature.data
            USER.introduction = form.introduction.data
            db.session.commit()
            return render_template("userInfo.html")
            # email = form.email.data
            # phone = form.phone.data
            # address = form.address.data
            # signature = form.signature.data
            # introduction = form.introduction.data


@bp.route('/userSetting')
@login_required
def userSetting():
    return render_template("userSetting.html")


@bp.route("/captcha", methods=['POST'])
def get_captcha():
    # GET,POST
    email = request.form.get("email")
    letters = string.ascii_letters + string.digits
    captcha = "".join(random.sample(letters, 4))
    if email:
        message = Message(
            subject="吃客行注册",
            recipients=[email],
            body=f"【吃客行】您的注册验证码是：{captcha}，请不要告诉任何人哦！"
        )
        mail.send(message)
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
        print("captcha:", captcha)
        # code: 200，成功的、正常的请求
        return jsonify({"code": 200})
    else:
        # code：400，客户端错误
        return jsonify({"code": 400, "message": "请先传递邮箱！"})
