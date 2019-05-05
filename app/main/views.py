from flask import (flash, g, redirect, render_template, request, session, url_for)
from peewee import *
from werkzeug.security import check_password_hash, generate_password_hash
from . import main
from .. import login_manager
from flask_login import login_required,current_user
from app.models import User,Secret,SubSecret

@main.route('/')
@login_required
def index():
    user = User.select().where(User.username==current_user.username).get()
    secrets = user.secrets
    subs = user.subSecrets
    return render_template('index.html',secrets=secrets,subs=subs)
