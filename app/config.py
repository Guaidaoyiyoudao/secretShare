import os


class Config(object):
    DEBUG = True
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_IMAGE_FOLDER = os.path.join(APP_ROOT, 'static/image/')
    SECRET_KEY = 'ABACADAS12312312312312312312'