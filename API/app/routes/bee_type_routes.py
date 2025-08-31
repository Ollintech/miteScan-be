from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from models.bee_type import BeeType
from auth.auth import get_current_user

bee_type_bp = Blueprint('bee_types', __name__, url_prefix='/bee-types')

@bee_type_bp.route('/', methods=['POST'])
@jwt_required()
def create_bee_type():
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        data = request.get_json()
        
        # Validate required fields
        if 'name' not in data:
            return jsonify({'error': 'Campo name é obrigatório'}), 400
        
        # Check if bee type already exists for this user
        existing_bee_type = BeeType.query.filter_by(name=data['name'], user_id=current_user.id).first()
        if existing_bee_type:
            return jsonify({'error': 'Tipo de abelha já existe'}), 400
        
        # Create new bee type
        new_bee_type = BeeType(
            name=data['name'],
            description=data.get('description'),
            user_id=current_user.id
        )
        
        db.session.add(new_bee_type)
        db.session.commit()
        
        return jsonify({
            'message': 'Tipo de abelha criado com sucesso',
            'bee_type': new_bee_type.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bee_type_bp.route('/', methods=['GET'])
@jwt_required()
def list_bee_types():
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Admin can see all bee types, users only their own
        if current_user.access_id == 1:
            bee_types = BeeType.query.all()
        else:
            bee_types = BeeType.query.filter_by(user_id=current_user.id).all()
        
        return jsonify({
            'bee_types': [bee_type.to_dict() for bee_type in bee_types]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bee_type_bp.route('/<int:bee_type_id>', methods=['GET'])
@jwt_required()
def get_bee_type(bee_type_id):
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        bee_type = BeeType.query.get(bee_type_id)
        if not bee_type:
            return jsonify({'error': 'Tipo de abelha não encontrado'}), 404
        
        # Users can only see their own bee types, admins can see any
        if bee_type.user_id != current_user.id and current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        return jsonify({'bee_type': bee_type.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bee_type_bp.route('/<int:bee_type_id>', methods=['PUT'])
@jwt_required()
def update_bee_type(bee_type_id):
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        bee_type = BeeType.query.get(bee_type_id)
        if not bee_type:
            return jsonify({'error': 'Tipo de abelha não encontrado'}), 404
        
        # Users can only update their own bee types, admins can update any
        if bee_type.user_id != current_user.id and current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        data = request.get_json()
        
        # Update allowed fields
        if 'name' in data:
            # Check if name is already taken by another bee type for this user
            existing_bee_type = BeeType.query.filter(
                BeeType.name == data['name'], 
                BeeType.user_id == bee_type.user_id,
                BeeType.id != bee_type_id
            ).first()
            if existing_bee_type:
                return jsonify({'error': 'Nome já está em uso'}), 400
            bee_type.name = data['name']
        if 'description' in data:
            bee_type.description = data['description']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Tipo de abelha atualizado com sucesso',
            'bee_type': bee_type.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bee_type_bp.route('/<int:bee_type_id>', methods=['DELETE'])
@jwt_required()
def delete_bee_type(bee_type_id):
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        bee_type = BeeType.query.get(bee_type_id)
        if not bee_type:
            return jsonify({'error': 'Tipo de abelha não encontrado'}), 404
        
        # Users can only delete their own bee types, admins can delete any
        if bee_type.user_id != current_user.id and current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        # Check if bee type is being used by hives
        if bee_type.hives:
            return jsonify({'error': 'Não é possível deletar tipo de abelha em uso por colmeias'}), 400
        
        db.session.delete(bee_type)
        db.session.commit()
        
        return jsonify({'message': 'Tipo de abelha deletado com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500