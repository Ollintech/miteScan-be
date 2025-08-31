from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.user import User
from models.company import Company
from models.access import Access
from auth.auth import get_password_hash, authenticate_user, create_user_token, get_current_user
from datetime import datetime

user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'password', 'access_id', 'company_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'Email já cadastrado'}), 400
        
        # Validate company exists
        company = Company.query.get(data['company_id'])
        if not company:
            return jsonify({'error': 'Empresa não encontrada'}), 400
        
        # Validate access level exists
        access = Access.query.get(data['access_id'])
        if not access:
            return jsonify({'error': 'Nível de acesso não encontrado'}), 400
        
        # Create new user
        new_user = User(
            name=data['name'],
            email=data['email'],
            password_hash=get_password_hash(data['password']),
            access_id=data['access_id'],
            company_id=data['company_id'],
            status=True
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'message': 'Usuário criado com sucesso',
            'user': new_user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400
        
        user = authenticate_user(data['email'], data['password'], db)
        if not user:
            return jsonify({'error': 'Credenciais inválidas'}), 401
        
        if not user.status:
            return jsonify({'error': 'Usuário inativo'}), 403
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Create token
        token = create_user_token(user.id)
        
        return jsonify({
            'access_token': token,
            'token_type': 'bearer',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user_info():
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        return jsonify({'user': current_user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/', methods=['GET'])
@jwt_required()
def list_users():
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Only admin can list all users
        if current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        users = User.query.all()
        return jsonify({
            'users': [user.to_dict() for user in users]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Users can only update themselves, admins can update anyone
        if current_user.id != user_id and current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            # Check if email is already taken by another user
            existing_user = User.query.filter(User.email == data['email'], User.id != user_id).first()
            if existing_user:
                return jsonify({'error': 'Email já está em uso'}), 400
            user.email = data['email']
        if 'status' in data and current_user.access_id == 1:  # Only admin can change status
            user.status = data['status']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Usuário atualizado com sucesso',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Only admin can delete users
        if current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Don't allow deleting yourself
        if user.id == current_user.id:
            return jsonify({'error': 'Não é possível deletar seu próprio usuário'}), 400
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'Usuário deletado com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500