from app import db
from models.company import Company
from models.user import User
from models.access import Access
from models.bee_type import BeeType
from models.hive import Hive
from models.hive_analysis import HiveAnalysis
from datetime import datetime
from auth.auth import get_password_hash

def seed_data():
    """Popula o banco de dados com dados iniciais"""
    try:
        print("🌱 Iniciando seed do banco de dados...")
        
        # Seed Access Levels
        access_levels = [
            {"name": "admin", "description": "Acesso de administrador com permissões ilimitadas"},
            {"name": "manager", "description": "Acesso de gerente com permissões limitadas"},
            {"name": "user", "description": "Acesso de usuário com permissões básicas"}
        ]
        
        for level in access_levels:
            existing_access = Access.query.filter_by(name=level["name"]).first()
            
            if not existing_access:
                new_access = Access(name=level["name"], description=level["description"])
                db.session.add(new_access)
                db.session.commit()
                print(f"✅ Nível de acesso '{level['name']}' criado com sucesso.")
                level["id"] = new_access.id
            else:
                level["id"] = existing_access.id
                print(f"ℹ️ Nível de acesso '{level['name']}' já existe.")

        # Seed Companies
        companies = [
            {
                "name": "MiteScan Corp", 
                "cnpj": "12345678901234", 
                "email": "admin@mitescan.com",
                "password": "admin123"
            },
            {
                "name": "BeeTech Solutions", 
                "cnpj": "23456789012345", 
                "email": "admin@beetech.com",
                "password": "beetech123"
            }
        ]
        
        for company_data in companies:
            existing_company = Company.query.filter_by(cnpj=company_data["cnpj"]).first()
            
            if not existing_company:
                new_company = Company(
                    name=company_data["name"], 
                    cnpj=company_data["cnpj"],
                    email=company_data["email"],
                    password_hash=get_password_hash(company_data["password"]),
                    access_id=1  # admin access
                )
                db.session.add(new_company)
                db.session.commit()
                print(f"✅ Empresa '{company_data['name']}' criada com sucesso.")
                company_data["id"] = new_company.id
            else:
                company_data["id"] = existing_company.id
                print(f"ℹ️ Empresa '{company_data['name']}' já existe.")

        # Seed Users
        users = [
            {
                "name": "Administrador",
                "email": "admin@mitescan.com",
                "password": "admin123",
                "access_id": 1,  # admin
                "company_id": companies[0]["id"]
            },
            {
                "name": "João Silva",
                "email": "joao@mitescan.com",
                "password": "joao123",
                "access_id": 2,  # manager
                "company_id": companies[0]["id"]
            },
            {
                "name": "Maria Santos",
                "email": "maria@beetech.com",
                "password": "maria123",
                "access_id": 3,  # user
                "company_id": companies[1]["id"]
            }
        ]
        
        for user_data in users:
            existing_user = User.query.filter_by(email=user_data["email"]).first()
            
            if not existing_user:
                new_user = User(
                    name=user_data["name"],
                    email=user_data["email"],
                    password_hash=get_password_hash(user_data["password"]),
                    access_id=user_data["access_id"],
                    company_id=user_data["company_id"],
                    status=True
                )
                db.session.add(new_user)
                db.session.commit()
                print(f"✅ Usuário '{user_data['name']}' criado com sucesso.")
                user_data["id"] = new_user.id
            else:
                user_data["id"] = existing_user.id
                print(f"ℹ️ Usuário '{user_data['name']}' já existe.")

        # Seed Bee Types
        bee_types = [
            {
                "name": "Apis mellifera",
                "description": "Abelha europeia, mais comum na apicultura",
                "user_id": users[1]["id"]  # João Silva
            },
            {
                "name": "Apis mellifera scutellata",
                "description": "Abelha africanizada",
                "user_id": users[1]["id"]
            },
            {
                "name": "Melipona quadrifasciata",
                "description": "Mandaçaia - abelha sem ferrão",
                "user_id": users[2]["id"]  # Maria Santos
            }
        ]
        
        for bee_type_data in bee_types:
            existing_bee_type = BeeType.query.filter_by(
                name=bee_type_data["name"], 
                user_id=bee_type_data["user_id"]
            ).first()
            
            if not existing_bee_type:
                new_bee_type = BeeType(
                    name=bee_type_data["name"],
                    description=bee_type_data["description"],
                    user_id=bee_type_data["user_id"]
                )
                db.session.add(new_bee_type)
                db.session.commit()
                print(f"✅ Tipo de abelha '{bee_type_data['name']}' criado com sucesso.")
                bee_type_data["id"] = new_bee_type.id
            else:
                bee_type_data["id"] = existing_bee_type.id
                print(f"ℹ️ Tipo de abelha '{bee_type_data['name']}' já existe.")

        # Seed Hives
        hives = [
            {
                "user_id": users[1]["id"],  # João Silva
                "bee_type_id": bee_types[0]["id"],
                "location_lat": -23.5505,
                "location_lng": -46.6333,
                "size": 10,
                "humidity": 65.0,
                "temperature": 24.5
            },
            {
                "user_id": users[1]["id"],
                "bee_type_id": bee_types[1]["id"],
                "location_lat": -23.5515,
                "location_lng": -46.6343,
                "size": 8,
                "humidity": 62.0,
                "temperature": 25.0
            },
            {
                "user_id": users[2]["id"],  # Maria Santos
                "bee_type_id": bee_types[2]["id"],
                "location_lat": -22.9068,
                "location_lng": -43.1729,
                "size": 6,
                "humidity": 70.0,
                "temperature": 23.8
            }
        ]
        
        for hive_data in hives:
            existing_hive = Hive.query.filter_by(
                user_id=hive_data["user_id"],
                location_lat=hive_data["location_lat"],
                location_lng=hive_data["location_lng"]
            ).first()
            
            if not existing_hive:
                new_hive = Hive(
                    user_id=hive_data["user_id"],
                    bee_type_id=hive_data["bee_type_id"],
                    location_lat=hive_data["location_lat"],
                    location_lng=hive_data["location_lng"],
                    size=hive_data["size"],
                    humidity=hive_data["humidity"],
                    temperature=hive_data["temperature"]
                )
                db.session.add(new_hive)
                db.session.commit()
                print(f"✅ Colmeia criada com sucesso (ID: {new_hive.id}).")
                hive_data["id"] = new_hive.id
            else:
                hive_data["id"] = existing_hive.id
                print(f"ℹ️ Colmeia já existe (ID: {existing_hive.id}).")

        # Seed Sample Analyses
        sample_analyses = [
            {
                "hive_id": hives[0]["id"],
                "analysis_type": "mite_detection",
                "result": "Baixa infestação de ácaros detectada",
                "confidence_score": 0.85,
                "status": "completed"
            },
            {
                "hive_id": hives[1]["id"],
                "analysis_type": "health_check",
                "result": "Colmeia saudável",
                "confidence_score": 0.92,
                "status": "completed"
            }
        ]
        
        for analysis_data in sample_analyses:
            existing_analysis = HiveAnalysis.query.filter_by(
                hive_id=analysis_data["hive_id"],
                analysis_type=analysis_data["analysis_type"]
            ).first()
            
            if not existing_analysis:
                new_analysis = HiveAnalysis(
                    hive_id=analysis_data["hive_id"],
                    analysis_type=analysis_data["analysis_type"],
                    result=analysis_data["result"],
                    confidence_score=analysis_data["confidence_score"],
                    status=analysis_data["status"],
                    analysis_date=datetime.utcnow()
                )
                db.session.add(new_analysis)
                db.session.commit()
                print(f"✅ Análise de exemplo criada (Tipo: {analysis_data['analysis_type']}).")
            else:
                print(f"ℹ️ Análise de exemplo já existe (Tipo: {analysis_data['analysis_type']}).")

        print("🎉 Seed do banco de dados concluído com sucesso!")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro durante o seed do banco de dados: {e}")
        raise e

if __name__ == "__main__":
    # Para executar o seed diretamente
    from app import create_app
    
    app = create_app()
    with app.app_context():
        seed_data()