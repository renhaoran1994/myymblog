"""
author : Ger-Rr
配置文件模块
"""
import logging
import os
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
database_uri = 'mysql+pymysql://root:renhaoranrhr94@localhost:3306/ginger?charset=utf8'

class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'u54ar@nj%jfgjkemnm4r&5***53hjff')

    ADMIN_POST_PER_PAGE = 10
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BLUE_BLOG_THEME = {'perfect_blue': 'Perfect Blue', 'black_swan': 'Black Swan', 'journal': 'journal',
                       'sketchy': 'sketchy'}

    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_FILE_UPLOADER = 'admin.upload_image'
    CKEDITOR_ENABLE_CODESNIPPET = True
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TSL = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Bluelog Admin', MAIL_USERNAME)

    BLUELOG_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    BLUELOG_COMMENT_PER_PAGE = 15
    BLOG_POST_PER_PAGE = 10
    BLUELOG_EMAIL = os.getenv('BLUELOG_EMAIL')
    BLUELOG_POST_PER_PAGE = 10
    BLUELOG_ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'png', 'jpeg', 'gif', 'svg', 'psd', 'cdr']



class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = database_uri


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', database_uri)
    DEBUG = True
    LOG_LEVEL = logging.DEBUG

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', database_uri)
    LOG_LEVEL = logging.WARNING
    DEBUG = False

config={
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig
}


