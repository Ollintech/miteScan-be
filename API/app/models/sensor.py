from app import db
from datetime import datetime

class Sensor(db.Model):
    __tablename__ = 'sensors'

    id = db.Column(db.Integer, primary_key=True)
    hive_id = db.Column(db.Integer, db.ForeignKey('hives.id'), nullable=False)
    temperature = db.Column(db.Float, nullable=True)
    humidity = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sensor_type = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), nullable=True, default='active')

    def __repr__(self):
        return f'<Sensor {self.id} - Hive {self.hive_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'hive_id': self.hive_id,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'sensor_type': self.sensor_type,
            'status': self.status
        }