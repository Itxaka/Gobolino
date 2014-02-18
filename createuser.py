# -*- coding: utf-8 -*-

from models import User
from flask_peewee.auth import make_password
from peewee import IntegrityError
import sys

try:
    user = sys.argv[1]
    password = make_password(sys.argv[2])

except IndexError:
    print "You need to pass two arguments, the user and the password!"
    exit()
try:
    User.create(username=user, password=password)
except IntegrityError as error:
    print "The user seems to exist already:"
    print error