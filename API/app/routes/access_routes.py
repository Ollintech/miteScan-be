from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from models.access import Access
from auth.auth import get_current_user

access_bp = Blueprint('access', __name__, url_prefix='/access')

@access_bp.route('/', methods=['GET'])
@jwt_required()
def list_access_levels():
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Only admin can list access levels
        if current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        access_levels = Access.query.all()
        return jsonify({
            'access_levels': [access.to_dict() for access in access_levels]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@access_bp.route('/', methods=['POST'])
@jwt_required()
def create_access_level():
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Only admin can create access levels
        if current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Check if access level already exists
        existing_access = Access.query.filter_by(name=data['name']).first()
        if existing_access:
            return jsonify({'error': 'Nível de acesso já existe'}), 400
        
        # Create new access level
        new_access = Access(
            name=data['name'],
            description=data['description']
        )
        
        db.session.add(new_access)
        db.session.commit()
        
        return jsonify({
            'message': 'Nível de acesso criado com sucesso',
            'access': new_access.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@access_bp.route('/<int:access_id>', methods=['PUT'])
@jwt_required()
def update_access_level(access_id):
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Only admin can update access levels
        if current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        access = Access.query.get(access_id)
        if not access:
            return jsonify({'error': 'Nível de acesso não encontrado'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'name' in data:
            # Check if name is already taken by another access level
            existing_access = Access.query.filter(Access.name == data['name'], Access.id != access_id).first()
            if existing_access:
                return jsonify({'error': 'Nome já está em uso'}), 400
            access.name = data['name']
        if 'description' in data:
            access.description = data['description']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Nível de acesso atualizado com sucesso',
            'access': access.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@access_bp.route('/<int:access_id>', methods=['DELETE'])
@jwt_required()
def delete_access_level(access_id):
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Only admin can delete access levels
        if current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        access = Access.query.get(access_id)
        if not access:
            return jsonify({'error': 'Nível de acesso não encontrado'}), 404
        
        # Don't allow deleting admin access level
        if access_id == 1:
            return jsonify({'error': 'Não é possível deletar o nível de acesso de administrador'}), 400
        
        # Check if access level has users or companies
        if access.users or access.companies:
            return jsonify({'error': 'Não é possível deletar nível de acesso em uso'}), 400
        
        db.session.delete(access)
        db.session.commit()
        
        return jsonify({'message': 'Nível de acesso deletado com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500