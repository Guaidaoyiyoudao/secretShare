from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,FileField,IntegerField,SelectField,SelectMultipleField
from wtforms.validators import DataRequired,regexp

class SubUploadForm(FlaskForm):

    secret = SelectField("选择主秘密")
    submit = SubmitField("参与")




class SecUploadForm(FlaskForm):


    img = FileField("主密码图像",validators=[DataRequired()])
    shareNums = IntegerField("分享人数",validators=[DataRequired()])
    needNums = IntegerField("参数人数",validators=[DataRequired()])
    user = SelectMultipleField("分发给用户")
    submit = SubmitField("分发子秘密")
    
