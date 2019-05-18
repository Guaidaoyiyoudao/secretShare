import os


class Config(object):
    DEBUG = True
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_IMAGE_FOLDER = os.path.join(APP_ROOT, 'static/image/')
    SECRET_KEY = 'ABACADAS12312312312312312312'
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'guaidaoyiyoudao@163.com'
    MAIL_PASSWORD = 'Lkq690859155'
    MAIL_DEFAULT_SENDER = 'guaidaoyiyoudao@163.com'
