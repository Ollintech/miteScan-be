from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.Boolean, nullable=False, default=True)
    access_id = db.Column(db.Integer, db.ForeignKey('accesses.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    
    # Relationships
    access = db.relationship('Access', backref='users')
    company = db.relationship('Company', backref='users')
    hives = db.relationship('Hive', backref='user', lazy=True)
    bee_types = db.relationship('BeeType', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'status': self.status,
            'access_id': self.access_id,
            'company_id': self.company_id
        }