from datetime import datetime
from project.app import
 db

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))
    description = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # İlişkiler
    equipment = db.relationship('Equipment', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    activities = db.relationship('Activity', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, name, location, description, notes, created_by_id):
        self.name = name
        self.location = location
        self.description = description
        self.notes = notes
        self.created_by_id = created_by_id
    
    def __repr__(self):
        return f'<Project {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'description': self.description,
            'notes': self.notes,
            'created_at': self.created_at.strftime('%d.%m.%Y - %H:%M'),
            'created_by': self.creator.full_name if self.creator else None
        }
