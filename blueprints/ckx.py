from flask import Blueprint, render_template,session, g, request, redirect, url_for, flash
# from .decorators import login_required
from .forms import LoginForm
from models import User_setting
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
            user = User_setting.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect("/")
            else:
                flash("邮箱和密码不匹配！")
                return redirect(url_for("ckx.login"))
        else:
            flash("邮箱或密码格式错误！")
            return redirect(url_for("ckx.login"))


@bp.route('/register')
def register():
    return render_template("register.html")


@bp.route('/recipeDetail')
def recipeDetail():
    return render_template("recipeDetail.html")
