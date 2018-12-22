"""
author : Ger-Rr
"""
from app.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin


class Admin(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(20))
    _password = db.Column(db.String(128))
    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(100))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw):
        self._password = generate_password_hash(raw)


    def check_password(self,raw):
        return check_password_hash(self._password,raw)




class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(30), unique=True)
    posts = db.relationship('Post', back_populates='category')

    def delete(self):
        default_category = Category.query.get(1)
        posts = self.posts[:]
        with db.auto_commit():
            for post in posts:
                post.category = default_category
            db.session.delete(self)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade='all')
    can_comments = db.Column(db.Boolean,default=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
    replies = db.relationship('Comment', back_populates='replied', cascade='all')


class Link(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(20))
    url = db.Column(db.String(225))