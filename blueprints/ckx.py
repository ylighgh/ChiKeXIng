from flask import Blueprint, render_template, session, g, request, redirect, url_for, flash
# from .decorators import login_required
from .forms import UserModel, RegisterForm,LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db

# from sqlalchemy import or_

bp = Blueprint("ckx", __name__, url_prefix="/")


@bp.route('/')
def index():
    return render_template("index.html")


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect("/")
            else:
                flash("邮箱和密码不匹配！")
                return redirect(url_for("ckx.login"))
        else:
            flash("邮箱和密码不匹配！")
            return redirect(url_for("ckx.login"))


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        email = form.email.data
        username = form.username.data
        password = form.password.data
        hash_password = generate_password_hash(password)
        user = UserModel(email=email, username=username, password=hash_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("ckx.login"))

@bp.route("/logout")
def logout():
    # 清除session中所有的数据
    session.clear()
    return redirect(url_for('ckx.login'))


@bp.route('/recipeDetail')
def recipeDetail():
    return render_template("recipeDetail.html")
