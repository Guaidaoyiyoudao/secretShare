from flask import Flask, redirect, render_template, request, url_for,abort,flash
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message
from app.models import User, db,ResetPassword
from peewee import DoesNotExist

from app.auth import auth
from app.auth.forms import LoginForm, RegisterForm,ResetForm,ChangeForm
from app import mail


@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    
    if form.is_submitted():
        
        username = form.username.data
        password = form.password.data
        email = form.email.data
        try:
            user = User.select().where(User.username==form.username.data).get()
        except DoesNotExist as e:
            user = User(username=username,password=password,email=email)

            msg = Message(subject="secretShare - email verify",recipients=[user.email],body='click %s to finish verify'%url_for('auth.verify_email',_external=True,token=user.verify_token))
            mail.send(msg)

            user.save()
            flash("邮箱验证已经发送到 %s!"%email)
            return redirect(url_for('auth.login'))
            
        flash("用户名已存在")
        return redirect(url_for('auth.register'))

    return render_template('register.html',form=form)


@auth.route('/login',methods=['GET','POST'])
def login():

    form = LoginForm()
    
    if form.validate_on_submit():
        
        try:
            user = User.select().where(User.username==form.username.data).get()
        except DoesNotExist as e:
            flash("用户名不存在")
            return redirect(url_for('auth.login'))

        if user.check_password(user.password,form.password.data):
            if user.email_verified:
                login_user(user)
                return redirect(url_for('main.index'))
            else:
                flash('你的邮箱%s尚未认证,无法登录!'%user.email)
        else:
            flash('帐号或者密码错误')
    #登录了就直接重定向到首页
    elif current_user.is_authenticated and current_user.email_verified:
        return redirect(url_for('main.index'))
    

    return render_template("login.html",form=form)
@auth.route('/email_verify/<token>',methods=['GET'])
def verify_email(token):
    try:
        user = User.select().where(User.verify_token==token).get()
    except DoesNotExist as e:
        flash("用户名不存在")
        return redirect(url_for('auth.login'))
    if not user.email_verified:
        user.email_verified = True
        user.save()
        flash('邮箱 %s 验证成功,请完成登录'%user.email)

    return redirect(url_for('auth.login'))



@auth.route('/reset_password',methods=['GET','POST'])
def reset_password():
    form = ResetForm()

    if form.validate_on_submit():

        email = form.email.data
        try:
            user = User.select().where(User.email==email).get()
        except DoesNotExist as e:
            flash("邮箱不存在!")
            return redirect(url_for('auth.reset_password'))
        reset = ResetPassword(user=user)
        msg = Message(subject="secretShare - Reset Password",recipients=[user.email],body='click %s to reset password'%url_for('auth.change_password',_external=True,token=reset.token))
        mail.send(msg)
        reset.save()
        flash("更改密码的邮件已经发送到 %s!"%email)

    return render_template('reset_password.html',form=form)

@auth.route('/reset_password/<token>',methods=['GET','POST'])
def change_password(token):
    form = ChangeForm()
    
    if form.validate_on_submit():
        try:
            user = ResetPassword.select().where(ResetPassword.token==token).get().user
        except DoesNotExist as e:
            return redirect(url_for('auth.reset_password'))
        user.password = form.password.data
        user.save()
        if current_user.is_authenticated:
            logout()
        flash("密码更改成功,请用新密码登录!")
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('成功退出帐号，请重新登录！')
    return redirect(url_for('auth.login'))



@auth.before_request
def before_request():
    db.connect()

@auth.after_request
def after_request(response):
    db.close()
    return response