from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required,current_user

from . import auth
from .. import db
from .. import models

#TODO 完善注册功能
@auth.route('/register',methods=['GET','POST'])
def register():
    return "<h1>register</h1>"
#TODO 完善登录功能
@auth.route('/login',methods=['GET','POST'])
def login():
    return render_template("login.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))