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
    username = StringField('Username',validators=[DataRequired('请输入正确用户名'),Length(1,20,message='用户名长度在2-20位字符')])
    password = PasswordField('Password',validators=[DataRequired('请输入正确密码'),Length(8,128,message='密码长度在8-60位字符')])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login in ')


class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired(message='请填写文章标题'),Length(1,60)])
    categories = SelectField('Category',coerce=int,default=1)
    body = CKEditorField('Body',validators=[DataRequired(message='请填写文章正文')])
    submit = SubmitField('Submit')

    def __init__(self,*args,**kwargs):
        super(PostForm,self).__init__(*args,**kwargs)
        self.categories.choices=[(category.id,category.name) for category in
                                 Category.query.order_by(Category.name).all()]

class CategoryForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Length(1,30)])
    submit=SubmitField('Submit')

    def vaild_name(self,field):
        if Category.query.filter_by(name=field.data).fisrt():
            raise ValidationError('分类名已存在')

class CommentForm(FlaskForm):
    author = StringField('Name',validators=[DataRequired(message='请填写回复昵称'),Length(1,30,
                                            message='昵称长度在2-30个字符')])
    email = StringField('Email',validators=[DataRequired(message='请填写邮箱（管理员会隐藏邮箱）'),Length(1,254),
                                            Email(message='电子邮箱不符合规范，请重新输入电子邮箱不符合规范，请重新输入')])
    site = StringField('Site',validators=[Optional(),URL(),Length(0,255)])
    body = TextAreaField('Comment',validators=[DataRequired('请填写回复内容')])
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