import os

from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from app.config import Config
login_manager = LoginManager()
mail = Mail()
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


    #flask mail
    mail.init_app(app)
    
    #bp register
    from app.auth import auth
    app.register_blueprint(auth)

    from app.main import main
    app.register_blueprint(main)

    from app.api import api
    app.register_blueprint(api)


 
  
    return app

