"""
author : Ger-Rr
生成虚拟数据
"""
from app.extensions import db
from app.model import Admin,Category,Post,Comment
from faker import Faker
import random
from app import create_app


fake = Faker('zh_CN')

def fake_admin():
    '''
    生成管理员帐号
    '''
    with db.auto_commit():

        admin = Admin(
            username='ginger',
            blog_title='Myblog',
            blog_sub_title="hello world",
            name='Mima Kirigoe',
            about='Um, l, Mima Kirigoe, had a fun time as a member of CHAM...'
        )
        admin.password='helloflask'
        db.session.add(admin)

def fake_categoies(count=10):
    with db.auto_commit():
        category = Category()
        category.name = 'Default'
        db.session.add(category)

    for i in range(count):
        with db.auto_commit():
            category = Category(name=fake.word())
            db.session.add(category)


def fake_posts(count=50):
    for i in range(count):
        with db.auto_commit():
            post = Post(
                title=fake.sentence(),
                body=fake.text(200),
                category=Category.query.get(random.randint(1, Category.query.count())),
                timestamp=fake.date_time_this_year()
            )
            db.session.add(post)


def fake_comments(count=50):
    for i in range(count):
        with db.auto_commit():
                comment = Comment(
                    author=fake.name(),
                    email=fake.email(),
                    site=fake.url(),
                    body=fake.sentence(),
                    timestamp=fake.date_time_this_year(),
                    reviewed=True,
                    post=Post.query.get(random.randint(1, Post.query.count()))
                )
                db.session.add(comment)


    salt =  int(count*0.1)
    for i in range(salt):
        with db.auto_commit():
            comment = Comment(
                author=fake.name(),
                email=fake.email(),
                site=fake.url(),
                body=fake.sentence(),
                timestamp=fake.date_time_this_year(),
                reviewed=False,
                post=Post.query.get(random.randint(1, Post.query.count()))
            )
            db.session.add(comment)

    for i in range(salt):
        with db.auto_commit():
            comment = Comment(
                author='Mima Kirigoe',
                email='mima@example.com',
                site='example.com',
                body=fake.sentence(),
                timestamp=fake.date_time_this_year(),
                from_admin=True,
                reviewed=True,
                post=Post.query.get(random.randint(1, Post.query.count()))
            )
            db.session.add(comment)

    for i in range(salt):
        with db.auto_commit():
            comment = Comment(
                author=fake.name(),
                email=fake.email(),
                site=fake.url(),
                body=fake.sentence(),
                timestamp=fake.date_time_this_year(),
                reviewed=True,
                replied=Comment.query.get(random.randint(1, Comment.query.count())),
                post=Post.query.get(random.randint(1, Post.query.count()))
            )
            db.session.add(comment)


app = create_app()
with app.app_context():
    fake_admin()
    fake_categoies()
    fake_posts()
    fake_comments()