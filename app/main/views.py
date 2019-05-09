from flask import flash, g, redirect, render_template, request, session, url_for,current_app as app
from peewee import *
from werkzeug.security import check_password_hash, generate_password_hash
from . import main
from .. import login_manager
from flask_login import login_required,current_user
from app.models import User,Secret,SubSecret
from app.main.forms import SecUploadForm,SubUploadForm
from werkzeug.utils import secure_filename
import os


@main.route('/upload',methods=['GET','POST'])
@login_required
def upload():
    form = SecUploadForm()
    users = User.select()
    user_list = []
    for user in users:
        user_list.append((user.username,user.username))
    form.user.choices = user_list

    if form.validate_on_submit():
        print("hello")
        filename = secure_filename(form.img.data.filename)
        img = form.img.data
        img.save(os.path.join(app.config['UPLOAD_IMAGE_FOLDER'],filename))
        return '<h1>success</h1>'

    return render_template('upload.html',form=form)
@main.route('/')
@login_required
def index():
    user = User.select().where(User.username==current_user.username).get()
    secrets = user.secrets
    subs = user.subSecrets
    return render_template('index.html',secrets=secrets,subs=subs)