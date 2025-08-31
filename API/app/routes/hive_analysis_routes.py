from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from models.hive_analysis import HiveAnalysis
from models.hive import Hive
from auth.auth import get_current_user
from datetime import datetime

hive_analysis_bp = Blueprint('hive_analysis', __name__, url_prefix='/hive-analysis')

@hive_analysis_bp.route('/', methods=['POST'])
@jwt_required()
def create_hive_analysis():
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['hive_id', 'analysis_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Validate hive exists and user has access
        hive = Hive.query.get(data['hive_id'])
        if not hive:
            return jsonify({'error': 'Colmeia não encontrada'}), 404
        
        if hive.user_id != current_user.id and current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        # Create new hive analysis
        new_analysis = HiveAnalysis(
            hive_id=data['hive_id'],
            analysis_type=data['analysis_type'],
            result=data.get('result'),
            confidence_score=data.get('confidence_score'),
            image_path=data.get('image_path'),
            status=data.get('status', 'completed'),
            analysis_date=datetime.utcnow()
        )
        
        db.session.add(new_analysis)
        db.session.commit()
        
        return jsonify({
            'message': 'Análise de colmeia criada com sucesso',
            'analysis': new_analysis.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@hive_analysis_bp.route('/', methods=['GET'])
@jwt_required()
def list_hive_analyses():
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Query parameters
        hive_id = request.args.get('hive_id', type=int)
        analysis_type = request.args.get('analysis_type')
        limit = request.args.get('limit', 50, type=int)
        
        # Build query
        query = HiveAnalysis.query
        
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
                query = query.filter(HiveAnalysis.hive_id.in_(user_hive_ids))
        
        if analysis_type:
            query = query.filter_by(analysis_type=analysis_type)
        
        # Order by analysis_date descending and limit
        analyses = query.order_by(HiveAnalysis.analysis_date.desc()).limit(limit).all()
        
        return jsonify({
            'analyses': [analysis.to_dict() for analysis in analyses],
            'count': len(analyses)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@hive_analysis_bp.route('/<int:analysis_id>', methods=['GET'])
@jwt_required()
def get_hive_analysis(analysis_id):
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        analysis = HiveAnalysis.query.get(analysis_id)
        if not analysis:
            return jsonify({'error': 'Análise de colmeia não encontrada'}), 404
        
        # Verify user has access to this analysis's hive
        hive = analysis.hive
        if hive.user_id != current_user.id and current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        return jsonify({'analysis': analysis.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@hive_analysis_bp.route('/<int:analysis_id>', methods=['PUT'])
@jwt_required()
def update_hive_analysis(analysis_id):
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        analysis = HiveAnalysis.query.get(analysis_id)
        if not analysis:
            return jsonify({'error': 'Análise de colmeia não encontrada'}), 404
        
        # Verify user has access to this analysis's hive
        hive = analysis.hive
        if hive.user_id != current_user.id and current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        data = request.get_json()
        
        # Update allowed fields
        if 'analysis_type' in data:
            analysis.analysis_type = data['analysis_type']
        if 'result' in data:
            analysis.result = data['result']
        if 'confidence_score' in data:
            analysis.confidence_score = data['confidence_score']
        if 'image_path' in data:
            analysis.image_path = data['image_path']
        if 'status' in data:
            analysis.status = data['status']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Análise de colmeia atualizada com sucesso',
            'analysis': analysis.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@hive_analysis_bp.route('/<int:analysis_id>', methods=['DELETE'])
@jwt_required()
def delete_hive_analysis(analysis_id):
    try:
        current_user = get_current_user(db)
        if not current_user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        analysis = HiveAnalysis.query.get(analysis_id)
        if not analysis:
            return jsonify({'error': 'Análise de colmeia não encontrada'}), 404
        
        # Verify user has access to this analysis's hive
        hive = analysis.hive
        if hive.user_id != current_user.id and current_user.access_id != 1:
            return jsonify({'error': 'Acesso negado'}), 403
        
        db.session.delete(analysis)
        db.session.commit()
        
        return jsonify({'message': 'Análise de colmeia deletada com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@hive_analysis_bp.route('/types', methods=['GET'])
@jwt_required()
def get_analysis_types():
    """Retorna os tipos de análise disponíveis"""
    try:
        analysis_types = [
            {'type': 'mite_detection', 'description': 'Detecção de ácaros'},
            {'type': 'bee_count', 'description': 'Contagem de abelhas'},
            {'type': 'health_check', 'description': 'Verificação de saúde'},
            {'type': 'activity_level', 'description': 'Nível de atividade'},
            {'type': 'temperature_analysis', 'description': 'Análise de temperatura'},
            {'type': 'humidity_analysis', 'description': 'Análise de umidade'}
        ]
        
        return jsonify({'analysis_types': analysis_types}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500