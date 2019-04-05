import os

from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

login_manager = LoginManager()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'secret.sqlite'),
    )
    #bootstrap
    Bootstrap(app)

    #flask-login
    login_manager.init_app(app)
    login_manager.login_view='auth.login'

    #view register
    from .auth import auth
    app.register_blueprint(auth)

    from .main import main
    app.register_blueprint(main)


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    return app

