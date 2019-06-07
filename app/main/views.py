from flask import flash, g, redirect, render_template, request, session, url_for,send_file,current_app as app
from peewee import *
from werkzeug.security import check_password_hash, generate_password_hash
from . import main
from .. import login_manager
from flask_login import login_required,current_user
from app.models import User,Secret,SubSecret
from app.main.forms import SecUploadForm,SubUploadForm
from werkzeug.utils import secure_filename
import os
import hashlib
from PIL import Image
from app.algorithm.algorithm import *

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

        filename = secure_filename(form.img.data.filename)
        img = form.img.data
        name = form.name.data
        total = form.shareNums.data
        need = form.needNums.data
        users = form.user.data
        img_uri = os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], filename)
        img.save(img_uri)

        #获取图片的宽度和长度
        imgFile = Image.open(img_uri)
        size = imgFile.size
        width = size[0]
        height = size[1]  
        imgFile.close()

        #获取图片的MD5值imp
        img_hash = get_md5(img_uri)
        # 保存记录
        sec = Secret(owner=current_user.id,name=name,secretHash=img_hash,
                     shareNums=total,needNums=need,width=width,height=height)
        sec.save()
        
        #获得载体图像的路径
        carriers_folder = app.config['CARRIER_FOLDER']
        carries = [os.path.join(app.config['CARRIER_FOLDER'],x) for x in os.listdir(carriers_folder)]
        if len(carries)<total:
            for i in range(0,total-len(carries)):
                carries.append(carries[int(i%len(carries))])     
        subsecs = Getsubimage(img_uri,total,need,carries)
        count = 0
        subsecfiles=[]
        for i in subsecs:
            uri = os.path.join(app.config['UPLOAD_IMAGE_FOLDER'],img_hash+str(count)+'.bmp')
            i.save(uri)
            count += 1

            subsec_hash = get_md5(uri)
            subsec = SubSecret(user=current_user.id,secret=sec,subSecretHash=subsec_hash,
                                img = uri)
            subsec.save()


        return '<h1>success</h1>'

    return render_template('upload.html',form=form)
@main.route('/')
@login_required
def index():
    user = User.select().where(User.username==current_user.username).get()
    secrets = user.secrets
    subs = user.subSecrets
    return render_template('index.html',secrets=secrets,subs=subs)

@main.route('/download/<img>')
@login_required
def download(img):
    current_secret = SubSecret.select().where(user=current_user)

    img_name =os.path.basename(img)
    return send_file(img,attachment_filename=img_name,as_attachment=True)
    


def get_md5(uri):
    md = hashlib.md5()
    with open(uri, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md.update(chunk)
    return md.hexdigest()
    

