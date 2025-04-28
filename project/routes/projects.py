from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from models.project import Project
from models.activity import Activity
from models.comment import Comment
from models.equipment import Equipment
from forms.project import ProjectForm
from forms.comment import CommentForm

bp = Blueprint('projects', __name__, url_prefix='/projects')

@bp.route('/')
@login_required
def list():
    """Projelerin listesini göster"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')

    query = Project.query

    if search:
        query = query.filter(Project.name.contains(search) | 
                              Project.location.contains(search))

    projects = query.order_by(Project.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)

    return render_template('projects/list.html', 
                           title='Projeler', 
                           projects=projects,
                           search=search)

@bp.route('/<int:id>')
@login_required
def detail(id):
    """Proje detaylarını göster"""
    project = Project.query.get_or_404(id)
    equipment = project.equipment.all()
    comments = project.comments.order_by(Comment.created_at.desc()).all()
    activities = project.activities.order_by(Activity.created_at.desc()).all()
    comment_form = CommentForm()

    return render_template('projects/detail.html',
                           title=project.name,
                           project=project,
                           equipment=equipment,
                           comments=comments,
                           activities=activities,
                           comment_form=comment_form)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Yeni proje oluştur"""
    form = ProjectForm()

    if form.validate_on_submit():
        project = Project(
            name=form.name.data,
            location=form.location.data,
            description=form.description.data,
            notes=form.notes.data,
            created_by_id=current_user.id
        )

        db.session.add(project)
        db.session.commit()

        # Aktivite kaydı oluştur
        Activity.log_activity(
            action='add',
            entity_type='project',
            entity_id=project.id,
            description=f'"{project.name}" projesi oluşturuldu',
            user_id=current_user.id,
            project_id=project.id
        )

        flash(f'"{project.name}" projesi başarıyla oluşturuldu.', 'success')
        return redirect(url_for('projects.detail', id=project.id))

    return render_template('projects/create.html',
                           title='Yeni Proje',
                           form=form)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Projeyi düzenle"""
    project = Project.query.get_or_404(id)

    # Sadece admin veya projeyi oluşturan kişi düzenleyebilir
    if not getattr(current_user, 'is_admin', lambda: False)() and project.created_by_id != current_user.id:
        flash('Bu projeyi düzenleme yetkiniz yok.', 'danger')
        return redirect(url_for('projects.detail', id=project.id))

    form = ProjectForm(obj=project)

    if form.validate_on_submit():
        project.name = form.name.data
        project.location = form.location.data
        project.description = form.description.data
        project.notes = form.notes.data

        db.session.commit()

        # Aktivite kaydı oluştur
        Activity.log_activity(
            action='edit',
            entity_type='project',
            entity_id=project.id,
            description=f'"{project.name}" projesi düzenlendi',
            user_id=current_user.id,
            project_id=project.id
        )

        flash(f'"{project.name}" projesi başarıyla güncellendi.', 'success')
        return redirect(url_for('projects.detail', id=project.id))

    return render_template('projects/edit.html',
                           title=f'Düzenle: {project.name}',
                           form=form,
                           project=project)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Projeyi sil"""
    project = Project.query.get_or_404(id)

    # Sadece admin silebilir
    if not getattr(current_user, 'is_admin', lambda: False)():
        flash('Bu projeyi silme yetkiniz yok.', 'danger')
        return redirect(url_for('projects.detail', id=project.id))

    project_name = project.name

    # İlişkili ekipmanların resimlerini sil
    for equipment in project.equipment:
        if equipment.image_path:
            try:
                os.remove(os.path.join('static/uploads', equipment.image_path))
            except Exception as e:
                print(f"Resim silinirken hata oluştu: {e}")

    db.session.delete(project)
    db.session.commit()

    # Aktivite kaydı oluştur (proje_id olmadan)
    Activity.log_activity(
        action='delete',
        entity_type='project',
        entity_id=id,
        description=f'"{project_name}" projesi silindi',
        user_id=current_user.id
    )

    flash(f'"{project_name}" projesi başarıyla silindi.', 'success')
    return redirect(url_for('projects.list'))
