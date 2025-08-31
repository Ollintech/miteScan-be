from flask import Blueprint, request, jsonify
from app import db
from models.sensor import Sensor
from models.hive import Hive
from auth.auth import get_current_user
from flask_jwt_extended import jwt_required
from datetime import datetime

sensor_bp = Blueprint('sensors', __name__, url_prefix='/sensors')

@sensor_bp.route('/data', methods=['POST'])
def receive_sensor_data():
    """Endpoint para receber dados dos sensores via MQTT ou HTTP"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['hive_id', 'temperature', 'humidity']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Validate hive exists
        hive = Hive.query.get(data['hive_id'])
        if not hive:
            return jsonify({'error': 'Colmeia não encontrada'}), 404
        
        # Create sensor reading
        sensor_reading = Sensor(
            hive_id=data['hive_id'],
            temperature=data['temperature'],
            humidity=data['humidity'],
            sensor_type=data.get('sensor_type', 'DHT22'),
            status=data.get('status', 'active'),
            timestamp=datetime.utcnow()
        )
        
        db.session.add(sensor_reading)
        
        # Update hive with latest readings
        hive.temperature = data['temperature']
        hive.humidity = data['humidity']
        
        db.session.commit()
        
        print(f"📊 Dados do sensor recebidos - Colmeia: {data['hive_id']}, Temp: {data['temperature']}°C, Umidade: {data['humidity']}%")
        
        return jsonify({
            'status': 'success',
            'message': 'Dados do sensor recebidos com sucesso',
            'sensor_id': sensor_reading.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro ao processar dados do sensor: {e}")
        return jsonify({'error': str(e)}), 500

@sensor_bp.route('/data', methods=['GET'])
@jwt_required()
def get_sensor_data():
    """Obter dados dos sensores com filtros opcionais"""
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Query parameters
        hive_id = request.args.get('hive_id', type=int)
        limit = request.args.get('limit', 100, type=int)
        
        # Build query
        query = Sensor.query
        
        if hive_id:
            # Verify user has access to this hive
            hive = Hive.query.get(hive_id)
            if not hive:
                return jsonify({'error': 'Colmeia não encontrada'}), 404
            
            if hive.user_id != current_user.id and current_user.access_id != 1:
                return jsonify({'error': 'Acesso negado'}), 403
            
            query = query.filter_by(hive_id=hive_id)
        else:
            # If no hive_id specified, only show user's hives (unless admin)
            if current_user.access_id != 1:
                user_hive_ids = [hive.id for hive in current_user.hives]
                query = query.filter(Sensor.hive_id.in_(user_hive_ids))
        
        # Order by timestamp descending and limit
        sensors = query.order_by(Sensor.timestamp.desc()).limit(limit).all()
        
        return jsonify({
            'sensors': [sensor.to_dict() for sensor in sensors],
            'count': len(sensors)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sensor_bp.route('/data/<int:sensor_id>', methods=['GET'])
@jwt_required()
def get_sensor_reading(sensor_id):
    """Obter uma leitura específica do sensor"""
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        sensor = Sensor.query.get(sensor_id)
        if not sensor:
            return jsonify({'error': 'Leitura do sensor não encontrada'}), 404
        
        # Verify user has access to this sensor's hive
        hive = sensor.hive
        if hive.user_id != current_user.id and current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        return jsonify({'sensor': sensor.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sensor_bp.route('/data/<int:sensor_id>', methods=['DELETE'])
@jwt_required()
def delete_sensor_reading(sensor_id):
    """Deletar uma leitura do sensor (apenas admin)"""
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Only admin can delete sensor readings
        if current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        sensor = Sensor.query.get(sensor_id)
        if not sensor:
            return jsonify({'error': 'Leitura do sensor não encontrada'}), 404
        
        db.session.delete(sensor)
        db.session.commit()
        
        return jsonify({'message': 'Leitura do sensor deletada com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@sensor_bp.route('/stats/<int:hive_id>', methods=['GET'])
@jwt_required()
def get_hive_sensor_stats(hive_id):
    """Obter estatísticas dos sensores de uma colmeia"""
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        hive = Hive.query.get(hive_id)
        if not hive:
            return jsonify({'error': 'Colmeia não encontrada'}), 404
        
        # Verify user has access to this hive
        if hive.user_id != current_user.id and current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        # Get sensor statistics
        sensors = Sensor.query.filter_by(hive_id=hive_id).all()
        
        if not sensors:
            return jsonify({
                'hive_id': hive_id,
                'stats': {
                    'total_readings': 0,
                    'temperature': {'min': None, 'max': None, 'avg': None},
                    'humidity': {'min': None, 'max': None, 'avg': None}
                }
            }), 200
        
        temperatures = [s.temperature for s in sensors if s.temperature is not None]
        humidities = [s.humidity for s in sensors if s.humidity is not None]
        
        stats = {
            'total_readings': len(sensors),
            'temperature': {
                'min': min(temperatures) if temperatures else None,
                'max': max(temperatures) if temperatures else None,
                'avg': sum(temperatures) / len(temperatures) if temperatures else None
            },
            'humidity': {
                'min': min(humidities) if humidities else None,
                'max': max(humidities) if humidities else None,
                'avg': sum(humidities) / len(humidities) if humidities else None
            },
            'latest_reading': sensors[0].to_dict() if sensors else None
        }
        
        return jsonify({
            'hive_id': hive_id,
            'stats': stats
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint compatível com o sistema MQTT existente
@sensor_bp.route('/', methods=['POST'])
def sensor_mqtt_endpoint():
    """Endpoint compatível com o sistema MQTT existente"""
    return receive_sensor_data()