from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required,current_user
from . import auth
from app import db
from app import models
from .forms import RegisterForm,LoginForm




@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    
    if form.is_submitted():
        
        username = form.username.data
        password = form.password.data

        


        return redirect(url_for('auth.login'))

    return render_template('register.html',form=form)

#TODO 完善登录功能
@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.is_submitted():
            return redirect(url_for('main.index'))
    return render_template("login.html",form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))