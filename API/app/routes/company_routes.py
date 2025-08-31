from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from models.company import Company
from models.access import Access
from auth.auth import get_password_hash, get_current_user
from datetime import datetime

company_bp = Blueprint('companies', __name__, url_prefix='/companies')

@company_bp.route('/register', methods=['POST'])
def register_company():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'cnpj', 'email', 'password', 'access_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Check if company already exists
        existing_company = Company.query.filter_by(email=data['email']).first()
        if existing_company:
            return jsonify({'error': 'Email já cadastrado'}), 400
        
        existing_cnpj = Company.query.filter_by(cnpj=data['cnpj']).first()
        if existing_cnpj:
            return jsonify({'error': 'CNPJ já cadastrado'}), 400
        
        # Validate access level exists
        access = Access.query.get(data['access_id'])
        if not access:
            return jsonify({'error': 'Nível de acesso não encontrado'}), 400
        
        # Create new company
        new_company = Company(
            name=data['name'],
            cnpj=data['cnpj'],
            email=data['email'],
            password_hash=get_password_hash(data['password']),
            access_id=data['access_id']
        )
        
        db.session.add(new_company)
        db.session.commit()
        
        return jsonify({
            'message': 'Empresa criada com sucesso',
            'company': new_company.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@company_bp.route('/', methods=['GET'])
@jwt_required()
def list_companies():
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Only admin can list all companies
        if current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        companies = Company.query.all()
        return jsonify({
            'companies': [company.to_dict() for company in companies]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@company_bp.route('/<int:company_id>', methods=['GET'])
@jwt_required()
def get_company(company_id):
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Users can only see their own company, admins can see any
        if current_user.company_id != company_id and current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        company = Company.query.get(company_id)
        if not company:
            return jsonify({'error': 'Empresa não encontrada'}), 404
        
        return jsonify({'company': company.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@company_bp.route('/<int:company_id>', methods=['PUT'])
@jwt_required()
def update_company(company_id):
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Only admin can update companies
        if current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        company = Company.query.get(company_id)
        if not company:
            return jsonify({'error': 'Empresa não encontrada'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'name' in data:
            company.name = data['name']
        if 'email' in data:
            # Check if email is already taken by another company
            existing_company = Company.query.filter(Company.email == data['email'], Company.id != company_id).first()
            if existing_company:
                return jsonify({'error': 'Email já está em uso'}), 400
            company.email = data['email']
        if 'cnpj' in data:
            # Check if CNPJ is already taken by another company
            existing_cnpj = Company.query.filter(Company.cnpj == data['cnpj'], Company.id != company_id).first()
            if existing_cnpj:
                return jsonify({'error': 'CNPJ já está em uso'}), 400
            company.cnpj = data['cnpj']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Empresa atualizada com sucesso',
            'company': company.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@company_bp.route('/<int:company_id>', methods=['DELETE'])
@jwt_required()
def delete_company(company_id):
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Only admin can delete companies
        if current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        company = Company.query.get(company_id)
        if not company:
            return jsonify({'error': 'Empresa não encontrada'}), 404
        
        # Check if company has users
        if company.users:
            return jsonify({'error': 'Não é possível deletar empresa com usuários cadastrados'}), 400
        
        db.session.delete(company)
        db.session.commit()
        
        return jsonify({'message': 'Empresa deletada com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500