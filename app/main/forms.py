from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,FileField,IntegerField,SelectField,SelectMultipleField
from wtforms.validators import DataRequired,regexp,ValidationError,NumberRange
from wtforms.widgets import html5

class Compare(object):
    """
    Compares the values of two fields.

    """
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if field.data >= other.data:
            d = {
                'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
                'other_name': self.fieldname
            }
            message = self.message
            if message is None:
                message = field.gettext('分享人数必须小于参与人数!')

            raise ValidationError(message % d)

class SubUploadForm(FlaskForm):

    secret = SelectField("选择主秘密")
    submit = SubmitField("参与")




class SecUploadForm(FlaskForm):


    img = FileField("主密码图像",validators=[DataRequired(message="上传主秘密图像！")])
    shareNums = IntegerField("Share Number",validators=[DataRequired(),NumberRange(min=1,message="最小人数必须大于0")],widget=html5.NumberInput())
    needNums = IntegerField("Join Number",validators=[DataRequired(),NumberRange(min=1,message="最小人数必须大于0"),Compare('shareNums')],widget=html5.NumberInput())
    user = SelectMultipleField("分发给用户")
    submit = SubmitField("分发子秘密")



    
