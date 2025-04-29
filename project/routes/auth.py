from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
from project.app import db
from forms.auth import LoginForm

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        from project.models.user import User # تم نقل الاستيراد إلى هنا لمنع الاستيراد الدائري
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Geçersiz kullanıcı adı veya şifre', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        
        flash(f'Hoş geldiniz, {user.full_name}!', 'success')
        return redirect(next_page)
    
    return render_template('login.html', title='Giriş Yap', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'success')
    return redirect(url_for('auth.login'))

# مهم جداً: لو عندك دالة load_user يفضل نقلها لملف app.py أو utils منفصل، لتجنب أخطاء لاحقاً.
