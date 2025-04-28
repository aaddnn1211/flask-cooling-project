from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from project.app import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    full_name = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user')  # 'admin' veya 'user'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişkiler
    projects = db.relationship('Project', backref='creator', lazy='dynamic')
    equipment = db.relationship('Equipment', backref='creator', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    activities = db.relationship('Activity', backref='user', lazy='dynamic')
    
    def __init__(self, username, email, full_name, password, role='user'):
        self.username = username
        self.email = email
        self.full_name = full_name
        self.set_password(password)
        self.role = role
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
