from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,TextField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):

    username = TextField('username',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()]) 
    submit = SubmitField("注册")

class LoginForm(FlaskForm):

    username = TextField('username',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    submit = SubmitField("登录")