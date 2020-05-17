#-*- coding: UTF-8 -*-
import os
import configparser
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))


def get_redis_url():
    config = configparser.ConfigParser()
    config.read(r'conf/ProjectConfig.ini')
    return 'redis://:{password}@{host}:{port}/1'.format(
        host=config['redis-50mkw']['host'],
        port=config['redis-50mkw']['port'],
        password=config['redis-50mkw']['password'],
    )


class Config(object):
    # 缓存1秒钟
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)
    # 设置密钥，可以通过 base64.b64encode(os.urandom(48)) 来生成一个指定长度的随机字符串
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ff72bf399e654310add53d08a164f311'
    # 配置日志
    # LOG_LEVEL = "DEBUG"

    # 数据库的配置信息
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:Happy@001@127.0.0.1:3306/50mkw'
    SQLALCHEMY_BINDS = {
        '50mkw': 'mysql+pymysql://root:Happy@001@47.105.84.136:3306/50mkw',
        'migration': 'mysql+pymysql://root:Happy@001@127.0.0.1:3306/so1',
        'movie': 'mysql+pymysql://root:Happy@001@127.0.0.1:3306/movie'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLALCHEMY_ECHO = True

    # 定义文件上传保存的路径，在__init__.py文件所在目录创建media文件夹，用于保存上传的文件
    UP_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app/static/media/')
    USER_IMAGE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app/static/user/')  # 存放用户头像的路径
    REDIS_URL = get_redis_url()

    # 邮箱服务
    MAIL_SERVER = 'smtp.mxhichina.com'
    # MAIL_SERVER = 'smtp.50mkw.com'
    # MAIL_PORT = 25
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'patrick.yang@50mkw.com'
    MAIL_PASSWORD = 'Love@001'
    MAIL_FROMADDR = MAIL_USERNAME
    ADMINS = ['patrick.yang@50mkw.com']

    # session 配置
    # SESSION_TYPE = "redis"  # 指定 session 保存到 redis 中
    # SESSION_USE_SIGNER = True  # session_id 进行加密签名处理
    # SESSION_REDIS = redis.StrictRedis( host=REDIS_HOST, port=REDIS_PORT,db=1 )
    # PERMANENT_SESSION_LIFETIME = 24 * 60 * 60 # session 的有效期，单位是秒

    # Celery configuration
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
