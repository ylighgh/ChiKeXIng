from exts import db
from datetime import datetime


class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)
    phone = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    signature = db.Column(db.String(100), nullable=True)
    introduction = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(200), nullable=True)


class RecipeModel(db.Model):
    __tablename__ = "recipe"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_name = db.Column(db.String(200), nullable=True)
    recipe_introduction = db.Column(db.String(200), nullable=True)
    recipe_steps = db.Column(db.String(200), nullable=True)
    post_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    avatar = db.Column(db.String(200), nullable=True)

    author = db.relationship("UserModel", backref="recipe")


class CommentModel(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    recipe = db.relationship("RecipeModel", backref=db.backref("comments", order_by=create_time.desc()))
    author = db.relationship("UserModel", backref="comments")
