from flask import Flask, redirect, render_template, request, url_for,abort,flash
from flask_login import current_user, login_required, login_user, logout_user

from app.models import User, db
from peewee import DoesNotExist

from app.auth import auth
from app.auth.forms import LoginForm, RegisterForm



@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    
    if form.is_submitted():
        
        username = form.username.data
        password = form.password.data
        print("[log] 用户不存在，创建")    
        user = User(username=username,password=password)
        user.save()
            
        return redirect(url_for('auth.login'))

    return render_template('register.html',form=form)

#TODO 完善登录功能
@auth.route('/login',methods=['GET','POST'])
def login():

    form = LoginForm()

    
    if form.validate_on_submit():
        
        try:
            user = User.select().where(User.username==form.username.data).get()
        except DoesNotExist as e:
            flash("用户名不存在")
            return render_template("login.html",form=form)
        if user.check_password(user.password,form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
    #登录了就直接重定向到首页
    elif current_user.is_authenticated:
        return redirect(url_for('main.index'))
    

    return render_template("login.html",form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))



@auth.before_request
def before_request():
    db.connect()

@auth.after_request
def after_request(response):
    db.close()
    return response