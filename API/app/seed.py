from sqlalchemy.orm import Session
from db.database import SessionLocal
from models import company as CompanyModel
from models import user as UserModel
from models import access as AccessModel
from models import bee_type as BeeTypeModel
from models import hive as HiveModel
from models import sensor as SensorModel
from models import hive_analysis as AnalysisModel
from datetime import datetime
from core.auth import get_password_hash

def seed_data():
    db: Session = SessionLocal()
    try:

        access_levels = [
            {"name": "owner", "description": "Administrator access with unlimited permissions."},
            {"name": "manager", "description": "Manager access with limited permissions."},
            {"name": "employee", "description": "Employee access with limited permissions."}
        ]
        
        for level in access_levels:
            existing_access = db.query(AccessModel.Access).filter(AccessModel.Access.name == level["name"]).first()
            
            if not existing_access:
                new_access = AccessModel.Access(name=level["name"], description=level["description"])
                db.add(new_access)
                db.commit()
                print(f"Nível de acesso '{level['name']}' criado com sucesso.")
                level["id"] = new_access.id
                
            else:
                level["id"] = existing_access.id
                print(f"Nível de acesso '{level['name']}' já existe.")

        companies = [
            {"name": "MiteScan", "cnpj": "12345678901234"},
            {"name": "BeeTech", "cnpj": "23456789012345"}
        ]
        
        for company in companies:
            existing_company = db.query(CompanyModel.Company).filter(CompanyModel.Company.cnpj == company["cnpj"]).first()
            
            if not existing_company:
                new_company = CompanyModel.Company(name=company["name"], cnpj=company["cnpj"])
                db.add(new_company)
                db.commit()
                print(f"Empresa '{company['name']}' criada com sucesso.")
                company["id"] = new_company.id
                
            else:
                company["id"] = existing_company.id
                print(f"Empresa '{company['name']}' já existe.")
        
        users = [
            {"name": "Ana Flávia", "email": "ana@mitescan.com", "password_hash": get_password_hash("anaflavia123"), "access_id": access_levels[1]["id"], "company_id": companies[0]["id"], "status": True},
            {"name": "Isabely Lemos", "email": "isabely@mitescan.com", "password_hash": get_password_hash("isabely123"), "access_id": access_levels[1]["id"], "company_id": companies[0]["id"], "status": True},
            {"name": "Gustavo Lanna", "email": "gustavo@mitescan.com", "password_hash": get_password_hash("gustavo123"), "access_id": access_levels[1]["id"], "company_id": companies[0]["id"], "status": True},
            {"name": "Yasmin Pires", "email": "yasmin@mitescan.com", "password_hash": get_password_hash("yasmin123"), "access_id": access_levels[1]["id"], "company_id": companies[0]["id"], "status": True},
        ]

        for user in users:
            existing_user = db.query(UserModel.User).filter(UserModel.User.email == user["email"]).first()
            
            if not existing_user:
                new_user = UserModel.User(
                    name=user["name"],
                    email=user["email"],
                    password_hash=user["password_hash"],
                    access_id=user["access_id"],
                    company_id=user["company_id"],
                    status=user["status"]
                )
                db.add(new_user)
                db.commit()
                print(f"Usuário '{user['name']}' criado com sucesso.")
                user["id"] = new_user.id
                
            else:
                user["id"] = existing_user.id
                print(f"Usuário '{user['name']}' já existe.")
            
        bee_types = [
            {"name": "Jataí", "description": "A abelha Jataí é uma espécie de abelha sem ferrão nativa da região Sudeste e Sul do Brasil. Ela é conhecida por sua produção de mel de alta qualidade e é muito importante para a polinização de diversas plantas.", "user_id": users[0]["id"]},
            {"name": "Mandaçaia", "description": "A Mandaçaia é uma abelha sem ferrão, nativa da região Nordeste do Brasil. Ela é muito apreciada pela produção de mel e tem um papel fundamental na polinização das plantas locais.", "user_id": users[1]["id"]},
            {"name": "Uruçu", "description": "A Uruçu é uma espécie de abelha sem ferrão encontrada principalmente na região Centro-Oeste e Norte do Brasil. É uma abelha social que produz mel de excelente sabor e tem grande valor ecológico.", "user_id": users[2]["id"]},
            {"name": "Irapuca", "description": "A Irapuca é uma abelha sem ferrão nativa da região Sudeste do Brasil, conhecida por sua capacidade de adaptar-se bem ao ambiente e por sua importante contribuição para a biodiversidade local.", "user_id": users[3]["id"]},
        ]
        
        for bee_type in bee_types:
            existing_bee_type = db.query(BeeTypeModel.BeeType).filter(BeeTypeModel.BeeType.name == bee_type["name"]).first()
            
            if not existing_bee_type:
                new_bee_type = BeeTypeModel.BeeType(
                    name=bee_type["name"],
                    description=bee_type["description"],
                    user_id=bee_type["user_id"]
                )
                db.add(new_bee_type)
                db.commit()
                print(f"Tipo de abelha '{bee_type['name']}' criado com sucesso.")
                bee_type["id"] = new_bee_type.id
                
            else:
                bee_type["id"] = existing_bee_type.id
                print(f"Tipo de abelha '{bee_type['name']}' já existe.")

        hives = [
            {"user_id": users[0]["id"], "bee_type_id": bee_types[0]["id"], "location_lat": -23.5505, "location_lng": -46.6333, "size": 10, "humidity": 65.0, "temperature": 30.5},
            {"user_id": users[1]["id"], "bee_type_id": bee_types[1]["id"], "location_lat": -23.5506, "location_lng": -46.6334, "size": 10, "humidity": 65.0, "temperature": 30.5},
            {"user_id": users[2]["id"], "bee_type_id": bee_types[2]["id"], "location_lat": -23.5507, "location_lng": -46.6335, "size": 10, "humidity": 65.0, "temperature": 30.5},
            {"user_id": users[3]["id"], "bee_type_id": bee_types[3]["id"], "location_lat": -23.5508, "location_lng": -46.6336, "size": 10, "humidity": 65.0, "temperature": 30.5},
        ]
        
        for hive in hives:
            existing_hive = db.query(HiveModel.Hive).filter(HiveModel.Hive.location_lat == hive["location_lat"], HiveModel.Hive.location_lng == hive["location_lng"]).first()
            
            if not existing_hive:
                new_hive = HiveModel.Hive(
                    user_id=hive["user_id"],
                    bee_type_id=hive["bee_type_id"],
                    location_lat=hive["location_lat"],
                    location_lng=hive["location_lng"],
                    size=hive["size"],
                    humidity=hive["humidity"],
                    temperature=hive["temperature"]
                )
                db.add(new_hive)
                db.commit()
                print(f"Colmeia localizada em ({hive['location_lat'], hive['location_lng']}) criada com sucesso.")
                hive["id"] = new_hive.id
                
            else:
                hive["id"] = existing_hive.id
                print(f"Colmeia localizada em ({hive['location_lat'], hive['location_lng']}) já existe.")
                
        sensors = [
            {"hive_id": hives[0]["id"], "humidity": 65.0, "temperature": 30.5},
            {"hive_id": hives[1]["id"], "humidity": 65.0, "temperature": 30.5},
            {"hive_id": hives[2]["id"], "humidity": 65.0, "temperature": 30.5},
            {"hive_id": hives[3]["id"], "humidity": 65.0, "temperature": 30.5},
        ]
        
        for sensor in sensors:
            existing_sensor = db.query(SensorModel.Sensor).filter(SensorModel.Sensor.hive_id == sensor["hive_id"]).first()
            
            if not existing_sensor:
                new_sensor = SensorModel.Sensor(
                    hive_id=sensor["hive_id"],
                    humidity=sensor["humidity"],
                    temperature=sensor["temperature"]
                )
                db.add(new_sensor)
                db.commit()
                print(f"Leitura do sensor da colmeia {sensor['hive_id']} criada com sucesso.")
                sensor["id"] = new_sensor.id
                
            else:
                sensor["id"] = existing_sensor.id
                print(f"Leitura do sensor da colmeia {sensor['hive_id']} já existe.")

        analyses = [
            {"hive_id": hives[0]["id"], "user_id": users[0]["id"], "image_path": "image.jpg", "varroa_detected": True, "detection_confidence": 0.92, "created_at": datetime.utcnow()},
            {"hive_id": hives[1]["id"], "user_id": users[1]["id"], "image_path": "image.jpg", "varroa_detected": False, "detection_confidence": 0.92, "created_at": datetime.utcnow()},
            {"hive_id": hives[2]["id"], "user_id": users[2]["id"], "image_path": "image.jpg", "varroa_detected": True, "detection_confidence": 0.92, "created_at": datetime.utcnow()},
            {"hive_id": hives[3]["id"], "user_id": users[3]["id"], "image_path": "image.jpg", "varroa_detected": False, "detection_confidence": 0.92, "created_at": datetime.utcnow()},
        ]
        
        for analysis in analyses: 
            existing_analysis = db.query(AnalysisModel.HiveAnalysis).filter(AnalysisModel.HiveAnalysis.hive_id == analysis["hive_id"]).first()
            
            if not existing_analysis:
                new_analysis = AnalysisModel.HiveAnalysis(
                    hive_id=analysis["hive_id"],
                    user_id=analysis["user_id"],
                    image_path=analysis["image_path"],
                    varroa_detected=analysis["varroa_detected"],
                    detection_confidence=analysis["detection_confidence"],
                    created_at=analysis["created_at"]
                )
                db.add(new_analysis)
                db.commit()
                print(f"Análise da colmeia '{analysis['hive_id']}' criada com sucesso.")
                analysis["id"] = new_analysis.id
                
            else:
                analysis["id"] = existing_analysis.id
                print(f"Análise da colmeia '{analysis['hive_id']}' já existe.")

        print("Seed aplicada com sucesso.")
        
    except Exception as e:
        print("Erro ao aplicar a seed:", e)
        import traceback
        traceback.print_exc()
        db.rollback()
        
    finally:
        try:
            db.close()
        except Exception as e:
            print("Erro ao fechar a sessão do banco de dados: ", e)
