from app import db

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    cnpj = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    access_id = db.Column(db.Integer, db.ForeignKey('accesses.id'), nullable=False)
    
    # Relationships
    access = db.relationship('Access', backref='companies')

    def __repr__(self):
        return f'<Company {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cnpj': self.cnpj,
            'email': self.email,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'access_id': self.access_id
        }