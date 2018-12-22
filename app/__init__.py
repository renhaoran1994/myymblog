"""
author : Ger-Rr
"""
from flask import Flask,render_template,current_app
from flask_wtf.csrf import CSRFError
from app.extensions import db,ckeditor,mail,bootstrap,moment,login_manager,csrf
from .model import Admin,Category,Comment
from flask_login import current_user
import click
from app.settings import config
import logging
from logging.handlers import RotatingFileHandler


def create_app(config_name):
    app = Flask(__name__)
    setup_log(config_name)
    register_bp(app)
    # app.config.from_object('app.config.secure')
    # app.config.from_object('app.config.setting')
    app.config.from_object(config[config_name])
    register_plugin(app)
    register_template_context(app)
    register_commands(app)
    register_errors(app)
    return app

def setup_log(config_name):
    #设置日志的记录等级
    logging.basicConfig(level=config[config_name].LOG_LEVEL)
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler('logs/log',maxBytes=1024*1024*100,backupCount=10)
    #创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    #为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)

def register_bp(app):
    from app.blueprint.auth import auth_bp
    app.register_blueprint(auth_bp,url_prefix='/auth')
    from app.blueprint.admin import admin_bp
    app.register_blueprint(admin_bp,url_prefix='/admin')
    from app.blueprint.blog import blog_bp
    app.register_blueprint(blog_bp)


def register_plugin(app):
    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

def register_logging(app):
    pass

def register_extensions(app):
    pass

def register_commands(app):
    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(username, password):
        click.echo('Initializing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin:  # 如果数据库中已经有管理员记录就更新用户名和密码
            click.echo('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:  # 否则创建新的管理员记录
            click.echo('Creating the temporary administrator account...')
            admin = Admin(
                username=username,
                blog_title='Bluelog',
                blog_sub_title="No, I'm the real thing.",
                name='Admin',
                about='Anything about you.'
            )
            admin.set_password(password)
            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            click.echo('Creating the default category...')
            category = Category(name='Default')
            db.session.add(category)

        db.session.commit()
        click.echo('Done.')


def register_errors(app):

    @app.errorhandler(400)
    def bad_request(e):
        current_app.logger.error(e)
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        current_app.logger.error(e)
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        current_app.logger.error(e)
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        current_app.logger.error(e)
        return render_template('errors/400.html', description=e.description), 400




def register_shell_context(app):
    pass

def register_template_context(app):
    @app.context_processor
    def make_app_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(admin=admin,categories=categories,unread_comments=unread_comments)


