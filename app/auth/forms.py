from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,TextField
from wtforms.validators import DataRequired,Email,EqualTo


class RegisterForm(FlaskForm):

    username = TextField('username',validators=[DataRequired()])
    email = TextField('email',validators=[DataRequired(),Email()])
    password = PasswordField('password',validators=[DataRequired(),EqualTo('confirm', message='Passwords must match')])
    password_comfirm = PasswordField('confirm password',validators=[DataRequired()])
    submit = SubmitField("注册")

class LoginForm(FlaskForm):

    username = TextField('username',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    submit = SubmitField("登录")


#发送修改密码的邮件
class ResetForm(FlaskForm):

    email = TextField('email',validators=[DataRequired(),Email()])
    submit = SubmitField("Reset Password")

#更改密码
class ChangeForm(FlaskForm):

    password = PasswordField('password',validators=[DataRequired(),EqualTo('password_comfirm', message='Passwords must match')])
    password_comfirm = PasswordField('confirm password',validators=[DataRequired()])
    submit = SubmitField("Change Password")