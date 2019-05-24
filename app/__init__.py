from flask import Flask
from flask_login import LoginManager
import config
from app.exts import db
from flask_migrate import Migrate
#创建app应用,__name__是python预定义变量，被设置为使用本模块.
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
app.config.from_object(config)
migrate = Migrate(app, db)

# 登陆
login = LoginManager(app)
# 限制登陆
login.login_view = "login"
from app import routes, models
