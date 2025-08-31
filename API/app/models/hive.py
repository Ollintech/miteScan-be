from app import db

class Hive(db.Model):
    __tablename__ = 'hives'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    bee_type_id = db.Column(db.Integer, db.ForeignKey('bee_types.id'), nullable=True)
    location_lat = db.Column(db.Float, nullable=False)
    location_lng = db.Column(db.Float, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    humidity = db.Column(db.Float, nullable=True)
    temperature = db.Column(db.Float, nullable=True)
    
    # Relationships
    bee_type = db.relationship('BeeType', backref='hives')
    sensors = db.relationship('Sensor', backref='hive', lazy=True)
    analyses = db.relationship('HiveAnalysis', backref='hive', lazy=True)

    def __repr__(self):
        return f'<Hive {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'bee_type_id': self.bee_type_id,
            'location_lat': self.location_lat,
            'location_lng': self.location_lng,
            'size': self.size,
            'humidity': self.humidity,
            'temperature': self.temperature
        }