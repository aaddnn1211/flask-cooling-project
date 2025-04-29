from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from project.app import db
from models.comment import Comment
from models.activity import Activity
from forms.comment import CommentForm

bp = Blueprint('comments', __name__, url_prefix='/comments')

@bp.route('/add/project/<int:project_id>', methods=['POST'])
@login_required
def add_project_comment(project_id):
    """Projeye yorum ekle"""
    from models.project import Project
    
    project = Project.query.get_or_404(project_id)
    form = CommentForm()
    
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            project_id=project.id,
            created_by_id=current_user.id
        )
        
        db.session.add(comment)
        db.session.commit()
        
        # Aktivite kaydı oluştur
        Activity.log_activity(
            action='add',
            entity_type='comment',
            entity_id=comment.id,
            description=f'"{project.name}" projesine yorum eklendi',
            user_id=current_user.id,
            project_id=project.id
        )
        
        flash('Yorumunuz başarıyla eklendi.', 'success')
    
    return redirect(url_for('projects.detail', id=project.id))

@bp.route('/add/equipment/<int:equipment_id>', methods=['POST'])
@login_required
def add_equipment_comment(equipment_id):
    """Ekipmana yorum ekle"""
    from models.equipment import Equipment
    
    equipment = Equipment.query.get_or_404(equipment_id)
    form = CommentForm()
    
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            project_id=equipment.project_id,
            equipment_id=equipment.id,
            created_by_id=current_user.id
        )
        
        db.session.add(comment)
        db.session.commit()
        
        # Aktivite kaydı oluştur
        Activity.log_activity(
            action='add',
            entity_type='comment',
            entity_id=comment.id,
            description=f'"{equipment.name}" ekipmanına yorum eklendi',
            user_id=current_user.id,
            project_id=equipment.project_id
        )
        
        flash('Yorumunuz başarıyla eklendi.', 'success')
    
    return redirect(url_for('equipment.detail', id=equipment.id))

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Yorumu sil"""
    comment = Comment.query.get_or_404(id)
    
    # Sadece admin veya yorumu yazan kişi silebilir
    if not current_user.is_admin() and comment.created_by_id != current_user.id:
        flash('Bu yorumu silme yetkiniz yok.', 'danger')
        if comment.equipment_id:
            return redirect(url_for('equipment.detail', id=comment.equipment_id))
        else:
            return redirect(url_for('projects.detail', id=comment.project_id))
    
    project_id = comment.project_id
    equipment_id = comment.equipment_id
    
    db.session.delete(comment)
    db.session.commit()
    
    # Aktivite kaydı oluştur
    if equipment_id:
        description = f'Ekipman yorumu silindi'
        redirect_url = url_for('equipment.detail', id=equipment_id)
    else:
        description = f'Proje yorumu silindi'
        redirect_url = url_for('projects.detail', id=project_id)
    
    Activity.log_activity(
        action='delete',
        entity_type='comment',
        entity_id=id,
        description=description,
        user_id=current_user.id,
        project_id=project_id
    )
    
    flash('Yorum başarıyla silindi.', 'success')
    return redirect(redirect_url)
