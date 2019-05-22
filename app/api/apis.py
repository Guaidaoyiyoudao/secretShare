from flask import Flask,abort,jsonify
from flask_login import current_user, login_required, login_user, logout_user

from app.models import User,ResetPassword,Secret,SubSecret
from peewee import DoesNotExist

from app.api import api




@api.route('/users',methods=['GET'])
@login_required
def users():
    users = User.select()
    if users is None:
        abort(404)
    data = []
    for user in users:
        data.append({'id': user.id,'user': user.username})
    return jsonify({'users':data})



@api.route('/users/<int:id>',methods=['GET'])
@login_required
def user(id):
    query = User.select().where(User.id==id)
    if not query.exists():
        abort(404)
    user = query.get()
    data ={'id': user.id,'user': user.username}
    return jsonify({'user':data})


#仅用于获取自己的主秘密
@api.route('/secrets',methods=['GET'])
@login_required
def secrets():
    secrets = Secret.select().where(Secret.owner==current_user.id)
    if not secrets.exists():
        abort(404)
    data = []
    for secret in secrets:
        data.append({'id': secret.id,'secret': secret.name,'hash':secret.secretHash,
        'shareNums':secret.shareNums,'hasNums':secret.hasNums,'needNums':secret.needNums})
    return jsonify({'secrets':data})