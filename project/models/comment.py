from datetime import datetime
from project.app import
 db

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişkiler
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __init__(self, content, project_id, created_by_id, equipment_id=None):
        self.content = content
        self.project_id = project_id
        self.equipment_id = equipment_id
        self.created_by_id = created_by_id
    
    def __repr__(self):
        return f'<Comment {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at.strftime('%d.%m.%Y - %H:%M'),
            'project_id': self.project_id,
            'equipment_id': self.equipment_id,
            'author': self.author.full_name if self.author else None
        }
