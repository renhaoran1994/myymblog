"""
author : Ger-Rr
扩展模块
"""
from flask import current_app
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_mail import Mail
from contextlib import contextmanager
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect



class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            current_app.logger.error(e)
            raise e



db = SQLAlchemy()
bootstrap = Bootstrap()
ckeditor = CKEditor()
moment = Moment()
mail = Mail()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
login_manager.login_message = u'请先完成登录'

@login_manager.user_loader
def load_user(uid):
    from app.model import Admin
    user = Admin.query.get(int(uid))
    return user