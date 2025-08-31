from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from models.hive import Hive
from models.bee_type import BeeType
from auth.auth import get_current_user

hive_bp = Blueprint('hives', __name__, url_prefix='/hives')

@hive_bp.route('/', methods=['POST'])
@jwt_required()
def create_hive():
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['location_lat', 'location_lng', 'size']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Validate bee_type if provided
        if 'bee_type_id' in data and data['bee_type_id']:
            bee_type = BeeType.query.get(data['bee_type_id'])
            if not bee_type:
                return jsonify({'error': 'Tipo de abelha não encontrado'}), 400
        
        # Create new hive
        new_hive = Hive(
            user_id=current_user.id,
            bee_type_id=data.get('bee_type_id'),
            location_lat=data['location_lat'],
            location_lng=data['location_lng'],
            size=data['size'],
            humidity=data.get('humidity'),
            temperature=data.get('temperature')
        )
        
        db.session.add(new_hive)
        db.session.commit()
        
        return jsonify({
            'message': 'Colmeia criada com sucesso',
            'hive': new_hive.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@hive_bp.route('/', methods=['GET'])
@jwt_required()
def list_hives():
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Admin can see all hives, users only their own
        if current_user.access_id == 1:
            hives = Hive.query.all()
        else:
            hives = Hive.query.filter_by(user_id=current_user.id).all()
        
        return jsonify({
            'hives': [hive.to_dict() for hive in hives]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@hive_bp.route('/<int:hive_id>', methods=['GET'])
@jwt_required()
def get_hive(hive_id):
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        hive = Hive.query.get(hive_id)
        if not hive:
            return jsonify({'error': 'Colmeia não encontrada'}), 404
        
        # Users can only see their own hives, admins can see any
        if hive.user_id != current_user.id and current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        return jsonify({'hive': hive.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@hive_bp.route('/<int:hive_id>', methods=['PUT'])
@jwt_required()
def update_hive(hive_id):
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        hive = Hive.query.get(hive_id)
        if not hive:
            return jsonify({'error': 'Colmeia não encontrada'}), 404
        
        # Users can only update their own hives, admins can update any
        if hive.user_id != current_user.id and current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        data = request.get_json()
        
        # Update allowed fields
        if 'location_lat' in data:
            hive.location_lat = data['location_lat']
        if 'location_lng' in data:
            hive.location_lng = data['location_lng']
        if 'size' in data:
            hive.size = data['size']
        if 'humidity' in data:
            hive.humidity = data['humidity']
        if 'temperature' in data:
            hive.temperature = data['temperature']
        if 'bee_type_id' in data:
            if data['bee_type_id']:
                bee_type = BeeType.query.get(data['bee_type_id'])
                if not bee_type:
                    return jsonify({'error': 'Tipo de abelha não encontrado'}), 400
            hive.bee_type_id = data['bee_type_id']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Colmeia atualizada com sucesso',
            'hive': hive.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@hive_bp.route('/<int:hive_id>', methods=['DELETE'])
@jwt_required()
def delete_hive(hive_id):
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        hive = Hive.query.get(hive_id)
        if not hive:
            return jsonify({'error': 'Colmeia não encontrada'}), 404
        
        # Users can only delete their own hives, admins can delete any
        if hive.user_id != current_user.id and current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        db.session.delete(hive)
        db.session.commit()
        
        return jsonify({'message': 'Colmeia deletada com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@hive_bp.route('/<int:hive_id>/sensors', methods=['GET'])
@jwt_required()
def get_hive_sensors(hive_id):
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        hive = Hive.query.get(hive_id)
        if not hive:
            return jsonify({'error': 'Colmeia não encontrada'}), 404
        
        # Users can only see their own hives, admins can see any
        if hive.user_id != current_user.id and current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        sensors = hive.sensors
        return jsonify({
            'sensors': [sensor.to_dict() for sensor in sensors]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500