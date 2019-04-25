from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,FileField,IntegerField
from wtforms.validators import DataRequired,regexp

class SubUploadForm(FlaskForm):

    img = FileField("主密码图像",validators=[DataRequired()])
    shareNums = IntegerField("分享人数",validators=[DataRequired()])
    needNums = IntegerField("参数人数",validators=[DataRequired()])



class SecUploadForm(FlaskForm):
    pass
    
