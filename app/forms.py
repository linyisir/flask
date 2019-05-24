from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError,Email,EqualTo
from app.models import User




class LoginForm(FlaskForm):
    #dataqureqiuue  当你在表格输入而直接到下一个表格时会提示你输入

    username = StringField('用户名', validators=[DataRequired(message='请输入用户名')])
    password = PasswordField('密码', validators=[DataRequired(message='请输入密码')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField( '重复密码', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('注册')

    # 效验用户名是否重复
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("用户名重复了，请重新填写！")

    # 检验邮箱是否重复
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("邮箱重复了，请重新填写！")
