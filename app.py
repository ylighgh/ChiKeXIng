from flask import Flask, session, g ,render_template
from flask_migrate import Migrate
import config
from exts import db, mail

# 数据库配置
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
