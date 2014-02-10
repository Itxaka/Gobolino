# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Email, InputRequired, EqualTo


class RegisterForm(Form):
    username = TextField(validators=[InputRequired])
    password = PasswordField(validators=[InputRequired(), EqualTo("confirm", message="Passwords don't match")])
    confirm = PasswordField()
    email = TextField(validators=[Email])

class PullImage(Form):
    url = TextField()