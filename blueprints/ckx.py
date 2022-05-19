from flask import Blueprint, render_template, session, g, request, redirect, url_for, flash
# from .decorators import login_required
from decorators import login_required
from .forms import UserModel, RegisterForm, LoginForm, CommentForm
from werkzeug.security import generate_password_hash, check_password_hash
from models import RecipeModel, CommentModel
from exts import db

bp = Blueprint("ckx", __name__, url_prefix="/")


@bp.route('/')
def index():
    recipes = RecipeModel.query.order_by(db.text("-post_time")).limit(6)
    return render_template("index.html", recipes=recipes)


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


"""
@bp.route('/recipeDetail/<int:recipe_id>')
def recipeDetail(recipe_id):
    recipe = RecipeModel.query.get(RecipeModel.recipe_id)
    return render_template("recipeDetail.html", recipe=recipe)
"""


@bp.route('/recipeDetail/')
def recipeDetail():
    recipe_id = request.args.get('recipe_id', type=int, default=1)
    recipes = RecipeModel.query.filter(RecipeModel.id == recipe_id)
    comments = CommentModel.query.filter(CommentModel.recipe_id == recipe_id).order_by(db.text("-create_time"))
    count = CommentModel.query.filter(CommentModel.recipe_id == recipe_id).count()
    return render_template("recipeDetail.html", recipes=recipes, comments=comments, count=count)


@bp.route('/explore')
def explore():
    page = request.args.get('page', type=int, default=1)
    paginate = RecipeModel.query.order_by(db.text("-post_time")).paginate(page=int(page), per_page=6)
    return render_template("explore.html", recipes=paginate)


@bp.route("/search")
def search():
    page = request.args.get('page', type=int, default=1)
    q = request.args.get("q")
    recipes = RecipeModel.query.filter(RecipeModel.recipe_name.contains(q)).order_by(
        db.text("-post_time")).paginate(page=int(page), per_page=6)
    return render_template("explore.html", recipes=recipes)


@bp.route("/comment", methods=['POST'])
@login_required
def comment():
    recipe_id = request.args.get('recipe_id', type=int, default=1)
    form = CommentForm(request.form)
    if form.validate():
        user_id = session.get("user_id")
        content = form.content.data
        comment_model = CommentModel(content=content, author_id=user_id, recipe_id=recipe_id)
        db.session.add(comment_model)
        db.session.commit()
        flash("评论成功！")
        return redirect(url_for("ckx.recipeDetail", recipe_id=recipe_id))
    else:
        flash("请输入内容！")
        return redirect(url_for("ckx.recipeDetail", recipe_id=recipe_id))
