from flask import Flask, redirect, render_template, request, url_for,abort,flash
from flask_login import current_user, login_required, login_user, logout_user

from app.models import User, db
from peewee import DoesNotExist

from app.auth import auth
from app.auth.forms import LoginForm, RegisterForm

import logging



@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    
    if form.is_submitted():
        
        username = form.username.data
        password = form.password.data
        try:
            user = User.select().where(User.username==form.username.data).get()
        except DoesNotExist as e:
            user = User(username=username,password=password)
            user.save()
            flash("帐号注册成功 %s"%username)
            print("注册成功")
            logging.info("用户 %s 注册成功"%username)
            return redirect(url_for('auth.login'))
            
        flash("用户名已经存在，请输入其他用户名")
        return render_template("register.html",form=form)

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
            print("用户不存在")
            return render_template("login.html",form=form)
        if user.check_password(user.password,form.password.data):
            logging.info("用户 %s 登录成功"%user.username)
            login_user(user)
            print("登录成功")
            return redirect(url_for('main.index'))
        else:
            flash("帐号或密码错误!")
            print("登录失败!")
    #登录了就直接重定向到首页
    elif current_user.is_authenticated:
        logging.info("用户 %s 重定向到首页"%current_user.username)
        return redirect(url_for('main.index'))
    

    return render_template("login.html",form=form)

@auth.route('/logout')
@login_required
def logout():
    logging.info("用户 %s logout"%current_user.username)
    logout_user()
    flash('你已经成功登出!')
    return redirect(url_for('auth.login'))



@auth.before_request
def before_request():
    db.connect()

@auth.after_request
def after_request(response):
    db.close()
    return response