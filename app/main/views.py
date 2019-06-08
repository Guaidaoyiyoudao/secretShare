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
        img_uri = os.path.join(app.config['TEMP_IMAGE_FOLDER'], filename)
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
        #子秘密图像生成
        subsecs = Getsubimage(img_uri,total,need,carries)
        #删除图片
        os.remove(img_uri)
        #获取分发的用户
        users = form.user.data



        count = 0
        subsecfiles=[]
        for i in subsecs:
            uri = os.path.join(app.config['UPLOAD_IMAGE_FOLDER'],img_hash+str(count)+'.bmp')
            i.save(uri)

            user = User.select().where(User.username==users[count]).get()

            subsec_hash = get_md5(uri)
            subsec = SubSecret(user=user.id,secret=sec,subSecretHash=subsec_hash,
                                img = uri)
            subsec.save()
            count += 1


        return redirect(url_for('main.index'))

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
    current_secret = SubSecret.select().where(SubSecret.user==current_user.id,SubSecret.img==img).get()

    current_secret.saved = True
    current_secret.save()

    img_name =os.path.basename(img)
    return send_file(img,attachment_filename=img_name,as_attachment=True)
@main.route('/save/<int:secret>')
@login_required
def save(secret):
    sec = Secret.select().where(Secret.id==secret).get()
    subsecret = SubSecret.select().where(SubSecret.user==current_user.id).get()
    img = os.path.join(app.config['UPLOAD_IMAGE_FOLDER'],sec.name+'.bmp')
    img_name =os.path.basename(img)
    if subsecret.secret != sec:
        return '<h1>未通过身份验证！</h1>'
    
    return send_file(img,attachment_filename=img_name,as_attachment=True)

@main.route('/recover',methods=['GET','POST'])
@login_required
def recover():
    form = SubUploadForm()
    
    if form.validate_on_submit():
        filename = secure_filename(form.img.data.filename)
        img = form.img.data
        tempuri = os.path.join(app.config['TEMP_IMAGE_FOLDER'],filename)
        img.save(tempuri)
        md5 = get_md5(tempuri)
        os.remove(tempuri)
        try:
            sub:SubSecret = SubSecret.select().where(SubSecret.subSecretHash==md5,SubSecret.user==current_user.id).get()
        
            #校验MD5值
    
            
            sub.uploaded = True
            sub.save()
            # 已有人数加1
            sub.secret.hasNums += 1
            sub.secret.save()

            if sub.secret.hasNums>=sub.secret.needNums:
                width = sub.secret.width
                height = sub.secret.height
                nums = sub.secret.needNums
                count = 0
                uris = []
                for sub in SubSecret.select().where(SubSecret.uploaded==True):
                    uris.append(sub.img)
                    count += 1
                    if count >= nums:
                        break
                secret_img = Getsecretimage(uris,width,height)

                secret_img.save(os.path.join(app.config['UPLOAD_IMAGE_FOLDER'],sub.secret.name+'.bmp'))
        except DoesNotExist as e:
            return '<h1>子秘密图像错误！(md5校验不通过)</h1>'
        flash('子秘密上传成功')
        return redirect(url_for('main.index'))
        
        



    
    return render_template('recover.html',form=form)

@main.route('/delete/<int:id>',methods=['GET'])
@login_required
def delete(id):
    sec = Secret.select().where(Secret.id==id).get()
    
    if sec.owner == current_user:
        sec.delete_instance(recursive=True)
        flash("秘密删除成功！")
    else:
        print(sec.owner,current_user.id)
        flash('身份验证不通过！')
    
    return redirect(url_for('main.index'))

def get_md5(uri):
    md = hashlib.md5()
    with open(uri, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md.update(chunk)
    return md.hexdigest()
    

