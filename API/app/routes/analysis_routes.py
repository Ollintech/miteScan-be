from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from models.analysis_backup import AnalysisBackup
from models.hive import Hive
from auth.auth import get_current_user
from datetime import datetime

analysis_bp = Blueprint('analysis', __name__, url_prefix='/analysis')

@analysis_bp.route('/', methods=['POST'])
@jwt_required()
def create_analysis_backup():
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['hive_id', 'analysis_data']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Validate hive exists and user has access
        hive = Hive.query.get(data['hive_id'])
        if not hive:
            return jsonify({'error': 'Colmeia não encontrada'}), 404
        
        if hive.user_id != current_user.id and current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        # Create new analysis backup
        new_analysis = AnalysisBackup(
            hive_id=data['hive_id'],
            analysis_data=data['analysis_data'],
            status=data.get('status', 'completed'),
            backup_date=datetime.utcnow()
        )
        
        db.session.add(new_analysis)
        db.session.commit()
        
        return jsonify({
            'message': 'Backup de análise criado com sucesso',
            'analysis': new_analysis.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/', methods=['GET'])
@jwt_required()
def list_analysis_backups():
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Query parameters
        hive_id = request.args.get('hive_id', type=int)
        limit = request.args.get('limit', 50, type=int)
        
        # Build query
        query = AnalysisBackup.query
        
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
                query = query.filter(AnalysisBackup.hive_id.in_(user_hive_ids))
        
        # Order by backup_date descending and limit
        analyses = query.order_by(AnalysisBackup.backup_date.desc()).limit(limit).all()
        
        return jsonify({
            'analyses': [analysis.to_dict() for analysis in analyses],
            'count': len(analyses)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/<int:analysis_id>', methods=['GET'])
@jwt_required()
def get_analysis_backup(analysis_id):
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        analysis = AnalysisBackup.query.get(analysis_id)
        if not analysis:
            return jsonify({'error': 'Backup de análise não encontrado'}), 404
        
        # Verify user has access to this analysis's hive
        hive = analysis.hive
        if hive.user_id != current_user.id and current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        return jsonify({'analysis': analysis.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/<int:analysis_id>', methods=['PUT'])
@jwt_required()
def update_analysis_backup(analysis_id):
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        analysis = AnalysisBackup.query.get(analysis_id)
        if not analysis:
            return jsonify({'error': 'Backup de análise não encontrado'}), 404
        
        # Verify user has access to this analysis's hive
        hive = analysis.hive
        if hive.user_id != current_user.id and current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        data = request.get_json()
        
        # Update allowed fields
        if 'analysis_data' in data:
            analysis.analysis_data = data['analysis_data']
        if 'status' in data:
            analysis.status = data['status']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Backup de análise atualizado com sucesso',
            'analysis': analysis.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/<int:analysis_id>', methods=['DELETE'])
@jwt_required()
def delete_analysis_backup(analysis_id):
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        analysis = AnalysisBackup.query.get(analysis_id)
        if not analysis:
            return jsonify({'error': 'Backup de análise não encontrado'}), 404
        
        # Verify user has access to this analysis's hive
        hive = analysis.hive
        if hive.user_id != current_user.id and current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        db.session.delete(analysis)
        db.session.commit()
        
        return jsonify({'message': 'Backup de análise deletado com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500