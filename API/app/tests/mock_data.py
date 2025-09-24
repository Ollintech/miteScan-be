# tests/mock_data.py
from datetime import datetime
from core.auth import get_password_hash

# ACCESS
def mock_access():
    return {
        "name": "Admin",
        "description": "Full system access"
    }


def mock_access_response():
    return {
        "id": 1,
        "name": "Admin",
        "description": "Full system access"
    }


# USER ROOT
def mock_user_root(access_id=1):
    return {
        "name": "Mock User",
        "email": "mockuser@example.com",
        "password": "securePass123",
        "access_id": access_id
    }


def mock_user_root_response():
    return {
        "id": 1,
        "name": "Mock User",
        "email": "mockuser@example.com",
        "status": True,
        "access_id": 1
    }
    
    
def mock_user_root_with_hash():
    user_root_data = mock_user_root()  # Gera os dados do usuário
    password = "securePass123"  # Senha fictícia
    user_root_data["password"] = password  # Adiciona a senha no mock
    user_root_data["password_hash"] = get_password_hash(password)  # Gera o hash da senha
    return user_root_data
    

# USER ASSOCIATED
def mock_user_associated(access_id=1, user_id=1):
    return {
        "name": "Mock User Associated",
        "email": "mockuser@example.com",
        "password": "securePass123",
        "access_id": access_id,
        "user_id": user_id
    }


def mock_user_associated_response():
    return {
        "id": 1,
        "name": "Mock User Associated",
        "email": "mockuser@example.com",
        "password": "securePass123",
        "access_id": 1,
        "user_id": 1
    }
    
    
def mock_user_associated_with_hash():
    user_root_data = mock_user()  # Gera os dados do usuário
    password = "securePass123"  # Senha fictícia
    user_root_data["password"] = password  # Adiciona a senha no mock
    user_root_data["password_hash"] = get_password_hash(password)  # Gera o hash da senha
    return user_root_data


# BEE TYPE
def mock_bee_type(user_id=1):
    return {
        "name": "Apis Mellifera",
        "description": "European honey bee",
        "user_id": user_id
    }


def mock_bee_type_response():
    return {
        "id": 1,
        "name": "Apis Mellifera",
        "description": "European honey bee",
        "user_id": 1
    }


# HIVE
def mock_hive(user_id=1, bee_type_id=1):
    return {
        "user_id": user_id,
        "bee_type_id": bee_type_id,
        "location_lat": -23.55052,
        "location_lng": -46.633308,
        "size": 10,
        "humidity": 55.5,
        "temperature": 34.2
    }


def mock_hive_response():
    return {
        "id": 1,
        "user_id": 1,
        "bee_type_id": 1,
        "location_lat": -23.55052,
        "location_lng": -46.633308,
        "size": 10,
        "humidity": 55.5,
        "temperature": 34.2
    }


# HIVE ANALYSIS
def mock_hive_analysis(hive_id=1, user_id=1):
    return {
        "hive_id": hive_id,
        "user_id": user_id,
        "image_path": "/images/hive_1.jpg",
        "varroa_detected": True,
        "detection_confidence": 0.92
    }


def mock_hive_analysis_response():
    return {
        "id": 1,
        "hive_id": 1,
        "user_id": 1,
        "image_path": "/images/hive_1.jpg",
        "varroa_detected": True,
        "detection_confidence": 0.92,
        "created_at": datetime(2024, 1, 1, 12, 0, 0)
    }


# ANALYSIS BACKUP
def mock_analysis_backup(analysis_id=1, user_id=1):
    return {
        "analysis_id": analysis_id,
        "user_id": user_id,
        "file_path": "/backups/analysis_1.json",
        "created_at": datetime(2024, 1, 1, 12, 5, 0)
    }


def mock_analysis_backup_response():
    return {
        "id": 1,
        "analysis_id": 1,
        "user_id": 1,
        "file_path": "/backups/analysis_1.json"
    }


# SENSOR
def mock_sensor_read(colmeia_id=1):
    return {
        "colmeia_id": colmeia_id,
        "temperature": 35.0,
        "humidity": 60.0
    }


def mock_sensor_response():
    return {
        "id": 1,
        "colmeia_id": 1,
        "temperature": 35.0,
        "humidity": 60.0
    }
