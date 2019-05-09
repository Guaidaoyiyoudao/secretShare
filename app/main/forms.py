from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,FileField,IntegerField,SelectField,SelectMultipleField
from wtforms.validators import DataRequired,regexp,ValidationError
from wtforms.widgets import html5

class SubUploadForm(FlaskForm):

    secret = SelectField("选择主秘密")
    submit = SubmitField("参与")




class SecUploadForm(FlaskForm):


    img = FileField("主密码图像",validators=[DataRequired(message="上传主秘密图像！")])
    shareNums = IntegerField("分享人数",validators=[DataRequired()],widget=html5.NumberInput())
    needNums = IntegerField("参与人数",validators=[DataRequired()],widget=html5.NumberInput())
    user = SelectMultipleField("分发给用户")
    submit = SubmitField("分发子秘密")

    def validate_neddNums(self,field):
    
        if field.needNums>field.shareNums:
            raise ValidationError('分享人数必须小于参与人数！')

    
