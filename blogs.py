"""
author : Ger-Rr
"""
import os
from dotenv import load_dotenv
from app import create_app
from app.extensions import db
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app.model import Admin,Category

dotenv_path = os.path.join(os.path.dirname(__file__),'.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app("production")
manager = Manager(app)
Migrate(app,db)
manager.add_command('db',MigrateCommand)

@manager.option('-u','username',dest='username')
@manager.option('-p','password',dest='password')
def create_user(username,password):
    if not all([username,password]):
        print('参数不足')
    admin = Admin.query.first()
    if admin:
        admin.username = username
        admin.password = password
    else:
        admin = Admin()
        admin.username = username
        admin.password = password
        admin.blog_title = '我的博客'
        admin.blog_sub_title = '博客子标题'
        admin.about = '这什么都没有'
        db.session.add(admin)
    categroy = Category.query.first()
    if categroy is None:
        print('创建初始分类')
        categroy = Category(name='默认')
        with db.auto_commit():
            db.session.add(categroy)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
