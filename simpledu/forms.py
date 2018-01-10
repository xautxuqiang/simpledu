from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email, EqualTo, Required, Regexp
from simpledu.models import db, User
from wtforms import ValidationError

class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[Required(), Length(3, 24, message='用户名长度要在3~24个字符之间'), Regexp('^[a-zA-Z0-9]+$', message='用户名只能为数字和字母')])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6, 24, message='密码长度要在6~24个字符之间')])
    repeat_password = PasswordField('重复密码', validators=[Required(), EqualTo('password', message='两次密码不一样')])
    submit = SubmitField('提交')

    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户已经存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')

class LoginForm(FlaskForm):
#    email = StringField('邮箱', validators=[Required(), Email()])
    username = StringField('用户名', validators=[Required(), Length(3,24)])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

#    def validate_email(self, field):
#        if field.data and not User.query.filter_by(email=field.data).first():
#            raise ValidationError('邮箱未注册')

    def validate_username(self, field):
        if field.data and not User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名未注册')

    def validate_password(self, field):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')
    

