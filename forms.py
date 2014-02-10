# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField, IntegerField, SelectField
from wtforms.validators import Email, InputRequired, EqualTo


class RegisterForm(Form):
    username = TextField(validators=[InputRequired])
    password = PasswordField(validators=[InputRequired(), EqualTo("confirm", message="Passwords don't match")])
    confirm = PasswordField()
    email = TextField(validators=[Email])


class PullImage(Form):
    url = TextField()


class NewContainer(Form):
    name = TextField(default=None)
    image = SelectField()
    command = TextField(default=None)
    entrypoint = TextField(default=None)
    hostname = TextField(default=None)
    detach = BooleanField(default=True)
    mem_limit = IntegerField(default=0)
    cpu_share = TextField(default=None)
    ports = TextField(default=None)
    dns = TextField(default=None)
    volumes = TextField(default=None)
    network_disabled = BooleanField(default=False)
    bind1 = TextField("Source", default=None)
    bind2 = TextField("Destination", default=None)

