from flask import Blueprint, render_template, g, request, redirect, url_for, flash
# from .decorators import login_required
# from .forms import QuestionFrom, AnswerFrom
from models import User_setting
from exts import db

# from sqlalchemy import or_

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route('/home')
def home():
    return render_template("home.html")


@bp.route('/postRecipe')
def postRecipe():
    return render_template("postRecipe.html")


@bp.route('/userRecipe')
def userRecipe():
    return render_template("userRecipe.html")


@bp.route('/userInfo')
def userInfo():
    return render_template("userInfo.html")


@bp.route('/userSetting')
def userSetting():
    return render_template("userSetting.html")
