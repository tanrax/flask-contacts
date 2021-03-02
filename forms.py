from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField('用户名', validators=[DataRequired(), Length(min=-1, max=30, message='用户名需要控制在30个字符以内')])
    password = StringField('密码1（公开）', validators=[DataRequired(), Length(min=-1, max=30, message='密码1（公开）需要控制在30个字符以内')])
    password2 = StringField('密码2（内部）', validators=[DataRequired(), Length(min=-1, max=30, message='密码2（内部）需要控制在30个字符以内')])

   # surname = StringField('Surname', validators=[Length(min=-1, max=100, message='You cannot have more than 100 characters')])
    # email = StringField('E-Mail', validators=[Email(), Length(min=-1, max=200, message='You cannot have more than 200 characters')])
    # phone = StringField('Phone', validators=[Length(min=-1, max=20, message='You cannot have more than 20 characters')])