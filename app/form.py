"""
author : Ger-Rr
"""
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,Length,ValidationError,Email,URL,Optional
from wtforms import StringField,SubmitField,PasswordField,BooleanField,SelectField,\
    TextAreaField,HiddenField
from flask_ckeditor import CKEditorField
from .model import Category


class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(1,20)])
    password = PasswordField('Password',validators=[DataRequired(),Length(8,128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login in ')


class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired(),Length(1,60)])
    categories = SelectField('Category',coerce=int,default=1)
    body = CKEditorField('Body',validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self,*args,**kwargs):
        super(PostForm,self).__init__(*args,**kwargs)
        self.categories.choices=[(category.id,category.name) for category in
                                 Category.query.order_by(Category.name).all()]

class CategoryForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Length(1,30)])
    submit=SubmitField()

    def vaild_name(self,field):
        if Category.query.filter_by(name=field.data).fisrt():
            raise ValidationError('Name already in use')

class CommentForm(FlaskForm):
    author = StringField('Name',validators=[DataRequired(),Length(1,30)])
    email = StringField('Email',validators=[DataRequired(),Length(1,254),Email()])
    site = StringField('Site',validators=[Optional(),URL(),Length(0,255)])
    body = TextAreaField('Comment',validators=[DataRequired()])
    submit = SubmitField('Submit')

class AdminComment(CommentForm):
    author =HiddenField()
    email = HiddenField()
    site = HiddenField()

class LinkForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Length(1,20)])
    url = StringField('Url',validators=[DataRequired(),Length(0,255)])
    submit = SubmitField('Submit')

class SettingForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Length(1,70)])
    blog_title = StringField('Blog Title',validators=[DataRequired(),Length(1,60)])
    blog_sub_title = StringField('Blog Sub Title',validators=[DataRequired(),Length(1,100)])
    about = CKEditorField('Body',validators=[DataRequired()])