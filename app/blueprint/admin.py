"""
author : Ger-Rr
"""
from flask import Blueprint,current_app,request,render_template,flash,url_for,redirect
import os
from app.utils import redirect_back,allowflie
from flask_login import login_required,current_user
from app.model import Post,Category,Comment,Link
from app.form import PostForm,CategoryForm,LinkForm,SettingForm
from app.extensions import db
from flask_ckeditor import upload_fail,upload_success
admin_bp = Blueprint('admin',__name__)

@admin_bp.before_request
@login_required
def login_protect():
    pass

@admin_bp.route('/setting',methods=['GET','POST'])
def settings():
    form = SettingForm()
    if form.validate_on_submit():
        with db.auto_commit():
            current_user.name = form.name.data
            current_user.blog_title = form.blog_title.data
            current_user.blog_sub_title = form.blog_sub_title.data
            current_user.about = form.about.data
        flash('资料修改成功','success')
        return redirect(url_for('blog.index'))

    form.name.data = current_user.name
    form.blog_title.data = current_user.blog_title
    form.blog_sub_title.data = current_user.blog_sub_title
    form.about.data = current_user.about
    return render_template('admin/settings.html',form=form)


@admin_bp.route('/post/manage')
def manage_post():
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['ADMIN_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp).paginate(
        page=page,per_page=per_page
    )
    posts = pagination.items
    return render_template('admin/manage_post.html',posts=posts,pagination=pagination)

@admin_bp.route('/post/new',methods=['GET','POST'])
def new_post():
    form = PostForm()
    if request.method=='POST' and form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.categories.data)
        post = Post()
        post.title = title
        post.category = category
        post.body = body
        try:
            db.session.add(post)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            raise e
        flash('新建了一篇文章','success')
        return redirect(url_for('blog.show_post',post_id=post.id))
    return render_template('admin/new_post.html',form=form)


@admin_bp.route('/post/int<post_id>/edit',methods=['GET','POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.categories.data)
        post.title = title
        post.body = body
        post.category = category
        with db.auto_commit():
            db.session.add(post)
        flash('修改成功','success')
        return redirect(url_for('blog.show_post',post_id=post_id))

    form.title.data = post.title
    form.body.data = post.body
    form.categories.data = post.category_id
    return render_template('admin/edit_post.html',form=form)

@admin_bp.route('/post/int<post_id>/delete',methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('删除文章成功','success')
    return redirect_back()


@admin_bp.route('/comment/manage')
def manage_comment():
    filter_file = request.args.get('filter','all')
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']

    if filter_file == 'uread':
        filter_comment = Comment.query.filter_by(reviewed=False)
    elif filter_file == 'admin':
        filter_comment = Comment.query.filter_by(from_admin=True)
    else:
        filter_comment = Comment.query
    pagination =  filter_comment.order_by(Comment.timestamp.desc()).paginate(
       page,per_page=per_page
    )
    comments = pagination.items
    return render_template('admin/manage_comment.html',comments=comments,pagination=pagination)


@admin_bp.route('/set_comment/int<post_id>',methods=['POST'])
def set_comment(post_id):
    post = Post.query.get_or_404(post_id)
    if post.can_comments:
        post.can_comments = False
        flash('已关闭评论','info')
    else:
        post.can_comments = True
        flash('已开启评论','info')
    db.session.commit()
    return redirect_back(url_for('blog.show_post',post_id=post_id))


@admin_bp.route('/comment/int<comment_id>/approve',methods=['POST'])
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.reviewed = True
    db.session.commit()
    flash('审核已通过','success')
    return redirect_back()

@admin_bp.route('/comment/int<comment_id>/delete',methods=['POST'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('评论删除成功','success')
    return redirect(url_for('.manage_comment'))


@admin_bp.route('/category/manage')
def manage_category():
    return render_template('admin/manage_category.html')

@admin_bp.route('/category/new',methods=['GET','POST'])
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category()
        category.name = name
        db.session.add(category)
        db.session.commit()
        flash('新增分类成功','success')
        return redirect(url_for('.manage_category'))
    return render_template('admin/new_category.html',form=form)

@admin_bp.route('/category/int<category_id>/edit',methods=['GET','POST'])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category_id == 1:
        flash('无法修改默认分类', 'warning')
        return redirect(url_for('.manage_category'))
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category.name = name
        db.session.commit()
        flash('修改分类成功','success')
        return redirect(url_for('.manage_category'))
    form.name.data = category.name
    return render_template('admin/edit_category.html',form=form)


@admin_bp.route('/category/int<category_id>/delete',methods=['POST'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.id ==1:
        flash('无法删除默认分类','warning')
        return redirect(url_for('blog.index'))
    category.delete()
    flash('删除分类成功','success')
    return redirect(url_for('.manage_category'))

@admin_bp.route('/link/manage')
def manage_link():
    return render_template('admin/manage_link.html')


@admin_bp.route('/link/new',methods=['GET','POST'])
def new_link():
    form = LinkForm()
    if form.validate_on_submit():
        name = form.name.data
        url = form.url.data
        link = Link()
        link.name = name
        link.url = url
        db.session.add(link)
        db.session.commit()
        flash('Link created.','success')
        return redirect(url_for('.manage_link'))
    return render_template('admin/new_link.html',form=form)


@admin_bp.route('/link/int<link_id>/edit',methods=['GET','POST'])
def edit_link(link_id):
    link = Link.query.get_or_404(link_id)
    form = LinkForm()
    if form.validate_on_submit():
        name = form.name.data
        url = form.url.data
        link.name = name
        link.url = url
        db.session.commit()
        flash('Link updated','success')
        return redirect(url_for('.manage_link'))
    form.name.data = link.name
    form.url.data = link.url

    return render_template('admin/edit_link.html',form=form)

@admin_bp.route('/link/int<link_id>/delete',methods=['GET','POST'])
def delete_link(link_id):
    link = Link.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    flash('link deleted','success')
    return redirect(url_for('.manage_link'))



@admin_bp.route('/upload',methods=['POST'])
def upload_image():
    f = request.files.get('upload')
    if not allowflie(f.filename):
        return upload_fail('请上传图片')
    f.save(os.path.join(current_app.config['BLUELOG_UPLOAD_PATH'],f.filename))
    url = url_for('blog.get_image',filename=f.filename)
    return upload_success(url,f.filename)
