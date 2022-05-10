from exts import db
from datetime import datetime


class User_setting(db.Model):
    # 表名
    __tablename__ = 'user_setting'
    # 字段名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(200), nullable=False)
    user_email = db.Column(db.String(200), nullable=False)
    user_password = db.Column(db.String(200), nullable=False)
