from flask_wtf import FlaskForm
from wtforms import StringField as _StringField, SubmitField as _SubmitField
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields.html5 import TelField as _TelField, EmailField as _EmailField

class AddArgsMixin(object):
    _field_args = {}

    def __init__(self, name, field_args=None, *args, **kwargs):
        self._field_args = field_args or {}                                
        super(AddArgsMixin, self).__init__(name, *args, **kwargs)

class StringField(AddArgsMixin, _StringField):
    pass


class SubmitField(AddArgsMixin, _SubmitField):
    pass


class TelField(AddArgsMixin, _TelField):
    pass


class EmailField(AddArgsMixin, _EmailField):
    pass

class ContactForm(FlaskForm):
    name = StringField('Name', dict(class_='form-control'), validators=[DataRequired(), Length(min=-1, max=80, message='You cannot have more than 80 characters')])
    surname = StringField('Surname', field_args=dict(class_='form-control'), validators=[
                          Length(min=-1, max=100, message='You cannot have more than 100 characters')])
    email = EmailField('E-Mail', field_args=dict(class_='form-control'), validators=[
                       Email(), Length(min=-1, max=200, message='You cannot have more than 200 characters')])
    phone = TelField('Phone', field_args=dict(class_='form-control'), validators=[
                     Length(min=-1, max=20, message='You cannot have more than 20 characters')])
    add = SubmitField('Add', field_args=dict(class_='btn btn-success'))

    
