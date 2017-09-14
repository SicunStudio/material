# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_principal import Principal

app = Flask(__name__)


app.config.from_object('config.DevelopmentConfig')  # 导入配置

# import production config
try:
    app.config.from_object('secret_config.ProductionConfig')
except:
    pass


db = SQLAlchemy(app)
principals = Principal(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
mail = Mail(app)


from material import views, models
