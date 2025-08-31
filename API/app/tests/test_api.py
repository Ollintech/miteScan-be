import pytest
import json
from app import create_app, db
from models.user import User
from models.company import Company
from models.access import Access

@pytest.fixture
def app():
    """Cria uma instância da aplicação para testes"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret'
    
    with app.app_context():
        db.create_all()
        
        # Criar dados de teste
        access = Access(name='admin', description='Admin access')
        db.session.add(access)
        db.session.commit()
        
        company = Company(
            name='Test Company',
            cnpj='12345678901234',
            email='test@company.com',
            password_hash='hashed_password',
            access_id=access.id
        )
        db.session.add(company)
        db.session.commit()
        
        yield app
        
        db.drop_all()

@pytest.fixture
def client(app):
    """Cliente de teste"""
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    """Headers de autenticação para testes"""
    # Criar usuário de teste
    with client.application.app_context():
        from auth.auth import get_password_hash
        
        user = User(
            name='Test User',
            email='test@user.com',
            password_hash=get_password_hash('testpass'),
            access_id=1,
            company_id=1,
            status=True
        )
        db.session.add(user)
        db.session.commit()
    
    # Fazer login
    response = client.post('/users/login', json={
        'email': 'test@user.com',
        'password': 'testpass'
    })
    
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}

def test_health_check(client):
    """Testa o endpoint de health check"""
    response = client.get('/')
    assert response.status_code == 200
    assert 'MiteScan API Flask is running!' in response.json['status']

def test_user_registration(client):
    """Testa o registro de usuário"""
    response = client.post('/users/register', json={
        'name': 'New User',
        'email': 'newuser@test.com',
        'password': 'newpass123',
        'access_id': 1,
        'company_id': 1
    })
    
    assert response.status_code == 201
    assert 'Usuário criado com sucesso' in response.json['message']

def test_user_login(client):
    """Testa o login de usuário"""
    # Primeiro registrar um usuário
    client.post('/users/register', json={
        'name': 'Login User',
        'email': 'login@test.com',
        'password': 'loginpass123',
        'access_id': 1,
        'company_id': 1
    })
    
    # Tentar fazer login
    response = client.post('/users/login', json={
        'email': 'login@test.com',
        'password': 'loginpass123'
    })
    
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_protected_route(client, auth_headers):
    """Testa uma rota protegida"""
    response = client.get('/users/me', headers=auth_headers)
    assert response.status_code == 200
    assert 'user' in response.json

def test_sensor_data_endpoint(client):
    """Testa o endpoint de dados do sensor"""
    # Primeiro criar uma colmeia
    with client.application.app_context():
        from models.hive import Hive
        hive = Hive(
            user_id=1,
            location_lat=-23.5505,
            location_lng=-46.6333,
            size=10
        )
        db.session.add(hive)
        db.session.commit()
    
    # Enviar dados do sensor
    response = client.post('/sensors/data', json={
        'hive_id': 1,
        'temperature': 25.5,
        'humidity': 60.2,
        'sensor_type': 'DHT22'
    })
    
    assert response.status_code == 201
    assert response.json['status'] == 'success'

def test_invalid_sensor_data(client):
    """Testa dados inválidos do sensor"""
    response = client.post('/sensors/data', json={
        'temperature': 25.5,
        'humidity': 60.2
        # hive_id ausente
    })
    
    assert response.status_code == 400
    assert 'hive_id' in response.json['error']

if __name__ == '__main__':
    pytest.main([__file__])