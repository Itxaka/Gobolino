# -*- coding: utf-8 -*-


class Configuration(object):
    DEBUG = True
    SECRET_KEY = ""
    HOST = "127.0.0.1"
    DOCKER_HOST = "unix://var/run/docker.sock"


class ConfigurationSqlite(Configuration):
    DATABASE = {
        'name': 'example.db',
        'engine': 'peewee.SqliteDatabase',
        'check_same_thread': False,
    }


class ConfigurationMysql(Configuration):
    DATABASE = {
        'name': '',
        'engine': 'peewee.MySQLDatabase',
        'host': '',
        'user': '',
        'passwd': '',
    }