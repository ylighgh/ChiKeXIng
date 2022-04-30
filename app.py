from flask import Flask, session, g, render_template
from flask_migrate import Migrate
import config
from exts import db, mail
from blueprints import ckx_bp
from happy_python import *

# 数据库配置
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)

# 绑定蓝图
app.register_blueprint(ckx_bp)

if __name__ == '__main__':
    app.run(port=8080)
