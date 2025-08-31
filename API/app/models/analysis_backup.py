from app import db
from datetime import datetime

class AnalysisBackup(db.Model):
    __tablename__ = 'analysis_backups'

    id = db.Column(db.Integer, primary_key=True)
    hive_id = db.Column(db.Integer, db.ForeignKey('hives.id'), nullable=False)
    analysis_data = db.Column(db.Text, nullable=True)
    backup_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=True, default='completed')
    
    # Relationships
    hive = db.relationship('Hive', backref='analysis_backups')

    def __repr__(self):
        return f'<AnalysisBackup {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'hive_id': self.hive_id,
            'analysis_data': self.analysis_data,
            'backup_date': self.backup_date.isoformat() if self.backup_date else None,
            'status': self.status
        }