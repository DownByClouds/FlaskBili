from flask import Flask
from config import Config
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager

#创建app应用,__name__是python预定义变量，被设置为使用本模块.
app = Flask(__name__)
#添加配置信息
app.config.from_object(Config)

login = LoginManager(app)
login.login_view = 'login'

#建立数据库关系
db = SQLAlchemy(app)
#绑定app和数据库，以便进行操作
# 使用--python myblog.py db 指令 --来操作
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# 要放在程序后面，只有先进行数据库绑定， 才能执行视图函数和数据库模型的相关操作
from app import routes, models