from datetime import datetime
import os
from project.app import db

class Equipment(db.Model):
    __tablename__ = 'equipment'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    description = db.Column(db.Text)
    notes = db.Column(db.Text)
    image_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişkiler
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    comments = db.relationship('Comment', backref='equipment', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, name, quantity, description, notes, image_path, category_id, project_id, created_by_id):
        self.name = name
        self.quantity = quantity
        self.description = description
        self.notes = notes
        self.image_path = image_path
        self.category_id = category_id
        self.project_id = project_id
        self.created_by_id = created_by_id
    
    def __repr__(self):
        return f'<Equipment {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'description': self.description,
            'notes': self.notes,
            'image_path': self.image_path,
            'created_at': self.created_at.strftime('%d.%m.%Y - %H:%M'),
            'category': self.category.name if self.category else None,
            'project': self.project.name if self.project else None,
            'created_by': self.creator.full_name if self.creator else None
        }
    
    @staticmethod
    def delete_image(image_path):
        """Ekipman silindiğinde ilişkili resmi de sil"""
        if image_path and os.path.exists(image_path):
            try:
                os.remove(image_path)
                return True
            except Exception as e:
                print(f"Resim silinirken hata oluştu: {e}")
                return False
        return False
