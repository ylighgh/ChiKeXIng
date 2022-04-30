from flask import Blueprint, render_template, g, request, redirect, url_for, flash
# from .decorators import login_required
# from .forms import QuestionFrom, AnswerFrom
# from models import QuestionModel, AnswerModel
from exts import db

# from sqlalchemy import or_

bp = Blueprint("ckx", __name__, url_prefix="/")


@bp.route('/')
def index():
    return render_template("index.html")


@bp.route('/login')
def login():
    return render_template("login.html")


@bp.route('/register')
def register():
    return render_template("register.html")
