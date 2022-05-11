from flask import Flask, session, g, render_template
from flask_migrate import Migrate
import config
from exts import db, mail
from blueprints import ckx_bp, user_bp
from models import UserModel
from happy_python import *

# 数据库配置
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)

# 绑定蓝图
app.register_blueprint(ckx_bp)
app.register_blueprint(user_bp)


@app.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            # 给g绑定一个叫做user的变量，他的值是user这个变量
            # setattr(g,"user",user)
            g.user = user
        except:
            g.user = None


@app.context_processor
def context_processor():
    if hasattr(g, "user"):
        return {"user": g.user}
    else:
        return {}


if __name__ == '__main__':
    app.run()
