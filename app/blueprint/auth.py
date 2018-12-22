"""
author : Ger-Rr
"""
from flask import Blueprint,abort,redirect,url_for,request,flash,render_template
from flask_login import login_user,current_user,logout_user,login_required
from app.form import LoginForm
from app.model import Admin
from app.utils import redirect_back

auth_bp = Blueprint('auth',__name__)

@auth_bp.route('login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            if admin.username == username and admin.check_password(password):
                login_user(admin,remember)
                flash('Welcome back','info')
                return redirect_back()
            flash('无效的用户名或者帐号','warning')
        else:
            flash('无效的帐号','warning')
    return render_template('auth/login.html',form=form)


@auth_bp.route('logout')
@login_required
def logout():
    logout_user()
    flash('Bye Master','info')
    return redirect_back()