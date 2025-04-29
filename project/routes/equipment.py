from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename
from project.app import db
from models.equipment import Equipment
from models.category import Category
from models.activity import Activity
from models.comment import Comment
from forms.equipment import EquipmentForm
from utils.file_handler import save_image, allowed_file

bp = Blueprint('equipment', __name__, url_prefix='/equipment')

from forms.comment import CommentForm  # تأكد أن هذا الاستيراد موجود فوق

@bp.route('/<int:id>')
@login_required
def detail(id):
    equipment = Equipment.query.get_or_404(id)
    comments = equipment.comments.order_by(Comment.created_at.desc()).all()
    comment_form = CommentForm()  # أنشئ نموذج إضافة تعليق فارغ
    
    return render_template('equipment/detail.html',
                          title=equipment.name,
                          equipment=equipment,
                          comments=comments,
                          comment_form=comment_form)  # أرسل النموذج إلى الصفحة


@bp.route('/create/<int:project_id>', methods=['GET', 'POST'])
@login_required
def create(project_id):
    """Yeni ekipman ekle"""
    from models.project import Project
    
    project = Project.query.get_or_404(project_id)
    categories = Category.query.all()
    
    form = EquipmentForm()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        image_filename = None
        
        if form.image.data:
            image_filename = save_image(form.image.data)
        
        equipment = Equipment(
            name=form.name.data,
            quantity=form.quantity.data,
            description=form.description.data,
            notes=form.notes.data,
            image_path=image_filename,
            category_id=form.category_id.data,
            project_id=project.id,
            created_by_id=current_user.id
        )
        
        db.session.add(equipment)
        db.session.commit()
        
        # Aktivite kaydı oluştur
        Activity.log_activity(
            action='add',
            entity_type='equipment',
            entity_id=equipment.id,
            description=f'"{equipment.name}" ekipmanı "{project.name}" projesine eklendi',
            user_id=current_user.id,
            project_id=project.id
        )
        
        flash(f'"{equipment.name}" ekipmanı başarıyla eklendi.', 'success')
        return redirect(url_for('projects.detail', id=project.id))
    
    return render_template('equipment/form.html',
                       title='Yeni Ekipman',
                       form=form,
                       project=project,
                       equipment=None)  # <-- أضف هذا


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Ekipmanı düzenle"""
    equipment = Equipment.query.get_or_404(id)
    
    # Sadece admin veya ekipmanı ekleyen kişi düzenleyebilir
    if not current_user.is_admin() and equipment.created_by_id != current_user.id:
        flash('Bu ekipmanı düzenleme yetkiniz yok.', 'danger')
        return redirect(url_for('equipment.detail', id=equipment.id))
    
    categories = Category.query.all()
    
    form = EquipmentForm(obj=equipment)
    form.category_id.choices = [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        equipment.name = form.name.data
        equipment.quantity = form.quantity.data
        equipment.description = form.description.data
        equipment.notes = form.notes.data
        equipment.category_id = form.category_id.data
        
        if form.image.data:
            # Eski resmi sil
            if equipment.image_path:
                Equipment.delete_image(os.path.join(current_app.config['UPLOAD_FOLDER'], equipment.image_path))
            
            # Yeni resmi kaydet
            equipment.image_path = save_image(form.image.data)
        
        db.session.commit()
        
        # Aktivite kaydı oluştur
        Activity.log_activity(
            action='edit',
            entity_type='equipment',
            entity_id=equipment.id,
            description=f'"{equipment.name}" ekipmanı düzenlendi',
            user_id=current_user.id,
            project_id=equipment.project_id
        )
        
        flash(f'"{equipment.name}" ekipmanı başarıyla güncellendi.', 'success')
        return redirect(url_for('equipment.detail', id=equipment.id))
    
    return render_template('equipment/form.html',
                          title=f'Düzenle: {equipment.name}',
                          form=form,
                          equipment=equipment,
                          project=equipment.project)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Ekipmanı sil"""
    equipment = Equipment.query.get_or_404(id)
    
    # Sadece admin veya ekipmanı ekleyen kişi silebilir
    if not current_user.is_admin() and equipment.created_by_id != current_user.id:
        flash('Bu ekipmanı silme yetkiniz yok.', 'danger')
        return redirect(url_for('equipment.detail', id=equipment.id))
    
    project_id = equipment.project_id
    equipment_name = equipment.name
    
    # Resmi sil
    if equipment.image_path:
        Equipment.delete_image(os.path.join(current_app.config['UPLOAD_FOLDER'], equipment.image_path))
    
    db.session.delete(equipment)
    db.session.commit()
    
    # Aktivite kaydı oluştur
    Activity.log_activity(
        action='delete',
        entity_type='equipment',
        entity_id=id,
        description=f'"{equipment_name}" ekipmanı silindi',
        user_id=current_user.id,
        project_id=project_id
    )
    
    flash(f'"{equipment_name}" ekipmanı başarıyla silindi.', 'success')
    return redirect(url_for('projects.detail', id=project_id))

@bp.route('/<int:id>/update-quantity', methods=['POST'])
@login_required
def update_quantity(id):
    """Ekipman miktarını güncelle (AJAX)"""
    equipment = Equipment.query.get_or_404(id)
    
    # Sadece admin veya ekipmanı ekleyen kişi güncelleyebilir
    if not current_user.is_admin() and equipment.created_by_id != current_user.id:
        return {'success': False, 'message': 'Yetkiniz yok'}, 403
    
    data = request.get_json()
    if not data or 'quantity' not in data:
        return {'success': False, 'message': 'Geçersiz veri'}, 400
    
    try:
        new_quantity = int(data['quantity'])
        if new_quantity < 0:
            return {'success': False, 'message': 'Miktar negatif olamaz'}, 400
        
        old_quantity = equipment.quantity
        equipment.quantity = new_quantity
        db.session.commit()
        
        # Aktivite kaydı oluştur
        Activity.log_activity(
            action='edit',
            entity_type='equipment',
            entity_id=equipment.id,
            description=f'"{equipment.name}" ekipmanının miktarı {old_quantity}\'den {new_quantity}\'e güncellendi',
            user_id=current_user.id,
            project_id=equipment.project_id
        )
        
        return {'success': True, 'quantity': new_quantity}
    except ValueError:
        return {'success': False, 'message': 'Geçersiz miktar'}, 400
