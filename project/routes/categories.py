from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from project.app import db
from project.models.category import Category
from project.models.activity import Activity
from project.forms.category import CategoryForm

bp = Blueprint('categories', __name__, url_prefix='/categories')

@bp.route('/')
@login_required
def list():
    """Kategorilerin listesini göster"""
    # سadece الادمن يمكنه مشاهدة الكاتيجوري
    if not current_user.is_admin():
        flash('Kategorileri görüntüleme yetkiniz yok.', 'danger')
        return redirect(url_for('index'))
    
    categories = Category.query.all()
    
    return render_template('categories/list.html',
                           title='Ekipman Kategorileri',
                           categories=categories)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Yeni kategori oluştur"""
    # سadece الادمن يمكنه إنشاء كاتيجوري
    if not current_user.is_admin():
        flash('Kategori oluşturma yetkiniz yok.', 'danger')
        return redirect(url_for('index'))
    
    form = CategoryForm()
    
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            description=form.description.data
        )
        
        db.session.add(category)
        db.session.commit()
        
        # تسجيل نشاط
        Activity.log_activity(
            action='add',
            entity_type='category',
            entity_id=category.id,
            description=f'"{category.name}" kategorisi oluşturuldu',
            user_id=current_user.id
        )
        
        flash(f'"{category.name}" kategorisi başarıyla oluşturuldu.', 'success')
        return redirect(url_for('categories.list'))
    
    return render_template('categories/form.html',
                           title='Yeni Kategori',
                           form=form,
                           category=None)  # مهم جدًا أن ترسل category=None هنا

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Kategoriyi düzenle"""
    # سadece الادمن يمكنه تعديل الكاتيجوري
    if not current_user.is_admin():
        flash('Kategori düzenleme yetkiniz yok.', 'danger')
        return redirect(url_for('index'))
    
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)
    
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        
        db.session.commit()
        
        # تسجيل نشاط
        Activity.log_activity(
            action='edit',
            entity_type='category',
            entity_id=category.id,
            description=f'"{category.name}" kategorisi düzenlendi',
            user_id=current_user.id
        )
        
        flash(f'"{category.name}" kategorisi başarıyla güncellendi.', 'success')
        return redirect(url_for('categories.list'))
    
    return render_template('categories/form.html',
                           title=f'Düzenle: {category.name}',
                           form=form,
                           category=category)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Kategoriyi sil"""
    # سadece الادمن يمكنه حذف الكاتيجوري
    if not current_user.is_admin():
        flash('Kategori silme yetkiniz yok.', 'danger')
        return redirect(url_for('index'))
    
    category = Category.query.get_or_404(id)
    
    # لا يمكن حذف كاتيجوري يحتوي على معدات
    if category.equipment.count() > 0:
        flash(f'"{category.name}" kategorisi kullanımda olduğu için silinemez.', 'danger')
        return redirect(url_for('categories.list'))
    
    category_name = category.name
    
    db.session.delete(category)
    db.session.commit()
    
    # تسجيل نشاط
    Activity.log_activity(
        action='delete',
        entity_type='category',
        entity_id=id,
        description=f'"{category_name}" kategorisi silindi',
        user_id=current_user.id
    )
    
    flash(f'"{category_name}" kategorisi başarıyla silindi.', 'success')
    return redirect(url_for('categories.list'))
