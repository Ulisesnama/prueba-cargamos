"""Configuración de desarrollo"""

# Utils
import os


param_dic = {
    "user": os.environ['POSTGRES_USER'],
    "password": os.environ['POSTGRES_PASSWORD'],
    "host": os.environ['POSTGRES_HOST'],
    "port": os.environ['POSTGRES_PORT'],
    "database": os.environ['POSTGRES_DB']
}


class Config:
    SECRET_KEY = 'ba093b9dd4e74151896dea10ae17c248'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = f'postgres://{param_dic.get("user")}:{param_dic.get("password")}@{param_dic.get("host")}:{param_dic.get("port")}/{param_dic.get("database")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True