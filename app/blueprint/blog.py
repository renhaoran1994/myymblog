"""
author : Ger-Rr
"""
from flask import Blueprint, render_template, current_app, request, url_for, flash, redirect, abort, make_response, \
    send_from_directory
from app.utils import redirect_back
from app.model import Post,Category,Comment,db
from flask_login import current_user
from app.form import AdminComment,CommentForm
from app.email import send_new_comment_email,send_new_reply_email

blog_bp = Blueprint('blog',__name__)

@blog_bp.route('/',defaults={'page':1})
@blog_bp.route('/page/<int:page>')
def index(page):
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page,per_page=per_page
    )
    posts = pagination.items
    return render_template('blog/index.html',pagination=pagination,posts=posts)

@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')

@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(
        page,per_page=per_page
    )
    posts = pagination.items
    return render_template('blog/category.html',pagination=pagination,posts=posts,category=category)



@blog_bp.route('/post/<int:post_id>',methods=['GET','POST'])
def show_post(post_id):
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    page = request.args.get('page',1,type=int)
    post = Post.query.get_or_404(post_id)
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(
        Comment.timestamp.desc()
    ).paginate(
        page,per_page=per_page
    )
    comments = pagination.items


    if current_user.is_authenticated:
        form = AdminComment()
        form.author.data = current_user.name
        form.email = current_app.config['BLUELOG_EMAIL']
        form.site.data = url_for('.index')
        from_admin = True
        reviewed =True
    else:
        form = CommentForm()
        from_admin =False
        reviewed = False
    if form.validate_on_submit() and post.can_comments:
        author = form.author.data
        if not isinstance(form.email,str):
            email = form.email.data
        else:
            email = form.email
        body = form.body.data
        site = form.site.data
        try:
            comment = Comment()
            comment.author = author
            comment.site = site
            comment.body = body
            comment.email = email
            comment.from_admin = from_admin
            comment.reviewed = reviewed
            comment.post = post
            replied_id = request.args.get('reply')
            if replied_id:
                replied_comment = Comment.query.get_or_404(replied_id)
                comment.replied = replied_comment
            db.session.add(comment)
            db.session.commit()
            if replied_id:
                replied_comment = Comment.query.get_or_404(replied_id)
                send_new_reply_email(replied_comment)
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            raise e
        if current_user.is_authenticated:
            flash('回复成功','success')
        else:
            flash('回复成功，回复内容将稍后显示', 'info')
            send_new_comment_email(post)
        return redirect(url_for('.show_post',post_id=post_id))
    return render_template('blog/post.html', post=post, comments=comments,
                               pagination=pagination,form=form)


@blog_bp.route('/reply_comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if not comment.post.can_comments:
        flash('当前文章不可评论','warning')
        return redirect(url_for('.show_post',post_id= comment.post.id))
    return redirect(url_for('.show_post',post_id=comment.post_id,reply=comment_id
                            ,author=comment.author)+'#comment-form')

@blog_bp.route('/change/<theme_name>')
def change_theme(theme_name):
    if theme_name not in current_app.config['BLUE_BLOG_THEME'].keys():
        abort(404)
    response = make_response(redirect_back())
    response.set_cookie('theme',theme_name,30*24*60*60)
    return response

@blog_bp.route('/uploads/<path:filename>')
def get_image(filename):
    return send_from_directory(current_app.config['BLUELOG_UPLOAD_PATH'],filename)