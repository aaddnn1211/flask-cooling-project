from datetime import datetime
from project.app import db

class Activity(db.Model):
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(50), nullable=False)  # 'add', 'edit', 'delete'
    entity_type = db.Column(db.String(50), nullable=False)  # 'project', 'equipment', 'comment'
    entity_id = db.Column(db.Integer)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişkiler
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    
    def __init__(self, action, entity_type, entity_id, description, user_id, project_id=None):
        self.action = action
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.description = description
        self.user_id = user_id
        self.project_id = project_id
    
    def __repr__(self):
        return f'<Activity {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'action': self.action,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'description': self.description,
            'created_at': self.created_at.strftime('%d.%m.%Y - %H:%M'),
            'user': self.user.full_name if self.user else None
        }
    
    @staticmethod
    def log_activity(action, entity_type, entity_id, description, user_id, project_id=None):
        """Aktivite kaydı oluştur ve veritabanına ekle"""
        activity = Activity(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            user_id=user_id,
            project_id=project_id
        )
        db.session.add(activity)
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Aktivite kaydı oluşturulurken hata: {e}")
            return False
