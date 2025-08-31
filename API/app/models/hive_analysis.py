from app import db
from datetime import datetime

class HiveAnalysis(db.Model):
    __tablename__ = 'hive_analyses'

    id = db.Column(db.Integer, primary_key=True)
    hive_id = db.Column(db.Integer, db.ForeignKey('hives.id'), nullable=False)
    analysis_type = db.Column(db.String(100), nullable=False)
    result = db.Column(db.Text, nullable=True)
    confidence_score = db.Column(db.Float, nullable=True)
    analysis_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_path = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), nullable=True, default='completed')

    def __repr__(self):
        return f'<HiveAnalysis {self.id} - {self.analysis_type}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'hive_id': self.hive_id,
            'analysis_type': self.analysis_type,
            'result': self.result,
            'confidence_score': self.confidence_score,
            'analysis_date': self.analysis_date.isoformat() if self.analysis_date else None,
            'image_path': self.image_path,
            'status': self.status
        }