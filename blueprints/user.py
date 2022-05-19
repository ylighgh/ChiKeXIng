import os.path
from datetime import datetime
from flask import Blueprint, render_template, g, request, session, redirect, url_for, flash, jsonify
from flask_mail import Message
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from models import EmailCaptchaModel, UserModel, RecipeModel, CommentModel
from decorators import login_required
from .forms import UserInfoFrom, UserSettingForm, PostRecipeForm, DeleteRecipeForm, UserAvatarForm, EditRecipeForm
import string
import random
from exts import db, mail
from config import UPLOAD_DIR

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route('/home')
@login_required
def home():
    return render_template("home.html")


@bp.route('/postRecipe', methods=['GET', 'POST'])
@login_required
def postRecipe():
    if request.method == 'GET':
        return render_template("postRecipe.html")
    else:
        form = PostRecipeForm(request.form, request.files)
        if form.validate():
            user_id = session.get("user_id")
            recipe_name = form.recipe_name.data
            recipe_introduction = form.recipe_introduction.data
            recipe_steps = form.recipe_steps.data
            avatar = request.files.get('avatar')
            # 保存到本地文件夹
            avatar_url = os.path.join(UPLOAD_DIR + 'recipe', avatar.filename)
            print(avatar_url)
            avatar.save(avatar_url)

            # 保存到数据库
            avatar_data = '/images/upload/recipe/' + avatar.filename

            recipe = RecipeModel(recipe_name=recipe_name, recipe_introduction=recipe_introduction,
                                 recipe_steps=recipe_steps, author_id=user_id, avatar=avatar_data)

            db.session.add(recipe)
            db.session.commit()
            flash("发布成功")
            return redirect(url_for("user.postRecipe"))


@bp.route('/userRecipe')
@login_required
def userRecipe():
    page = request.args.get('page', type=int, default=1)
    user_id = session.get("user_id")
    paginate = RecipeModel.query.filter(RecipeModel.author_id == user_id).order_by(
        db.text("-post_time")).paginate(page=int(page), per_page=5)
    return render_template("userRecipe.html", recipes=paginate)


# 搜索记录
@bp.route("/search")
def search():
    # /search?q=xxx
    page = request.args.get('page', type=int, default=1)
    q = request.args.get("q")
    user_id = session.get("user_id")
    # filter_by：直接使用字段的名称
    # filter：使用模型.字段名称
    recipes = RecipeModel.query.filter(or_(RecipeModel.recipe_name.contains(q), RecipeModel.id.contains(q)),
                                       RecipeModel.author_id == user_id).order_by(
        db.text("-post_time")).paginate(page=int(page), per_page=5)
    return render_template("userRecipe.html", recipes=recipes)


@bp.route('/userInfo', methods=['GET', 'POST'])
@login_required
def userInfo():
    if request.method == 'GET':
        user_id = session.get("user_id")
        count = RecipeModel.query.filter(RecipeModel.author_id == user_id).count()
        return render_template("userInfo.html", count=count)
    else:
        form = UserInfoFrom(request.form)
        if form.validate():
            # 获取当前用户的id值
            user_id = session.get("user_id")
            USER = UserModel.query.filter(UserModel.id == user_id).first()
            print(USER)
            USER.username = form.username.data
            USER.phone = form.phone.data
            USER.address = form.address.data
            USER.signature = form.signature.data
            USER.introduction = form.introduction.data
            db.session.commit()
            return render_template("userInfo.html")


@bp.route('/userSetting', methods=['GET', 'POST'])
@login_required
def userSetting():
    if request.method == 'GET':
        return render_template("userSetting.html")
    else:
        form = UserSettingForm(request.form)
        if form.validate():
            # 获取当前用户的id值
            user_id = session.get("user_id")
            USER = UserModel.query.filter(UserModel.id == user_id).first()
            oldPassword = form.oldPassword.data
            if check_password_hash(USER.password, oldPassword):
                USER.password = generate_password_hash(form.newPassword.data)
                db.session.commit()
                flash("修改成功")
                return render_template("userSetting.html")
            else:
                flash("旧密码错误，请重新输入")
                return redirect(url_for("user.userSetting"))
        else:
            flash("两次输入密码不一致，请重新输入")
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
        return jsonify({"code": 400, "message": "请先输入邮箱！"})


# 删除指定记录
@bp.route("/delete_recipe", methods=['POST'])
def delete_recipe():
    form = DeleteRecipeForm(request.form)
    recipe_id = form.recipe_id.data
    CommentModel.query.filter(CommentModel.recipe_id == recipe_id).delete()
    db.session.commit()
    RecipeModel.query.filter(RecipeModel.id == recipe_id).delete()
    db.session.commit()
    flash(f'成功删除编号为{recipe_id}的记录')
    return redirect(url_for('user.userRecipe'))


@bp.route("/avatarUpload", methods=['POST'])
def avatarUpload():
    form = UserAvatarForm(request.files)

    avatar = request.files.get('avatar')
    # 保存到本地文件夹
    avatar_url = os.path.join(UPLOAD_DIR + 'avatar', avatar.filename)
    print(avatar_url)
    avatar.save(avatar_url)
    # 保存到数据库
    user_id = session.get("user_id")
    USER = UserModel.query.filter(UserModel.id == user_id).first()
    USER.avatar = '/images/upload/avatar/' + avatar.filename
    db.session.commit()

    print(USER.avatar)
    return render_template("userInfo.html")


@bp.route('/editRecipe', methods=['GET', 'POST'])
@login_required
def editRecipe():
    if request.method == 'GET':
        recipe_id = request.args.get('recipe_id', type=int, default=1)
        recipes = RecipeModel.query.filter(RecipeModel.id == recipe_id)
        return render_template("editRecipe.html", recipes=recipes)
    else:
        form = EditRecipeForm(request.form, request.files)
        if form.validate():
            RECIPE = RecipeModel.query.filter(RecipeModel.id == form.recipe_id.data).first()
            RECIPE.recipe_name = form.recipe_name.data
            RECIPE.recipe_introduction = form.recipe_introduction.data
            RECIPE.recipe_steps = form.recipe_steps.data
            avatar = request.files.get('avatar')
            # 保存到本地文件夹
            avatar_url = os.path.join(UPLOAD_DIR + 'recipe', avatar.filename)
            avatar.save(avatar_url)
            # 保存到数据库
            RECIPE.avatar = '/images/upload/recipe/' + avatar.filename
            db.session.commit()
            flash("修改成功")
            return redirect(url_for("user.userRecipe"))
