import functools

from flask import Blueprint

api = Blueprint('api', __name__,url_prefix='/api')

from . import apis