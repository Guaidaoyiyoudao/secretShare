from flask import Flask, redirect, render_template, request, url_for,abort,flash
from flask_login import current_user, login_required, login_user, logout_user

from app.models import User, db,ResetPassword
from peewee import DoesNotExist

from app.api import api



@login_required
@api.route('/users',methods=['GET'])
def users():
    pass
