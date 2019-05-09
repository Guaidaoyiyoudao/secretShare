import os

from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from app.config import Config
login_manager = LoginManager()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    #bootstrap
    Bootstrap(app)

    #flask-login
    login_manager.init_app(app)
    login_manager.login_message ="你还没有登录，请先登录！"
    login_manager.login_view='auth.login'

    #bp register
    from .auth import auth
    app.register_blueprint(auth)

    from .main import main
    app.register_blueprint(main)


 
  
    return app

