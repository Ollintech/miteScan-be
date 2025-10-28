from sqlalchemy.orm import Session
from db.database import SessionLocal
from models import user_root as UserRootModel
from models import users_associated as UserAssociatedModel
from models import access as AccessModel
from models import bee_type as BeeTypeModel
from models import hive as HiveModel
from models import sensor_readings as SensorModel
from models import hive_analysis as AnalysisModel
from models import analysis_backup as AnalysisBackupModel
from datetime import datetime
from core.auth import get_password_hash

def seed_data():
    db: Session = SessionLocal()
    try:

        # --- 1. Níveis de Acesso ---
        access_levels_data = [
            {"name": "owner", "description": "Administrator access with unlimited permissions."},
            {"name": "manager", "description": "Manager access with limited permissions."},
            {"name": "employee", "description": "Employee access with limited permissions."}
        ]
        
        for level in access_levels_data:
            existing_access = db.query(AccessModel.Access).filter(AccessModel.Access.name == level["name"]).first()
            
            if not existing_access:
                new_access = AccessModel.Access(name=level["name"], description=level["description"])
                db.add(new_access)
                print(f"Nível de acesso '{level['name']}' criado com sucesso.")
            else:
                print(f"Nível de acesso '{level['name']}' já existe.")
        db.commit()

        # Buscar IDs após a criação
        owner_access_id = db.query(AccessModel.Access.id).filter(AccessModel.Access.name == "owner").scalar()
        manager_access_id = db.query(AccessModel.Access.id).filter(AccessModel.Access.name == "manager").scalar()
        employee_access_id = db.query(AccessModel.Access.id).filter(AccessModel.Access.name == "employee").scalar()

        # --- 2. Usuários Root ---
        root_users_data = [
            {"name": "Ana Flávia", "email": "ana@mitescan.com", "password_hash": get_password_hash("anaflavia123"), "status": True},
            {"name": "Isabely Lemos", "email": "isabely@mitescan.com", "password_hash": get_password_hash("isabely123"), "status": True},
            {"name": "Gustavo Lanna", "email": "gustavo@mitescan.com", "password_hash": get_password_hash("gustavo123"), "status": True},
            {"name": "Yasmin Pires", "email": "yasmin@mitescan.com", "password_hash": get_password_hash("yasmin123"), "status": True},
        ]

        for user in root_users_data:
            existing_user = db.query(UserRootModel.UserRoot).filter(UserRootModel.UserRoot.email == user["email"]).first()
            
            if not existing_user:
                new_user = UserRootModel.UserRoot(
                    name=user["name"],
                    email=user["email"],
                    password_hash=user["password_hash"],
                    access_id=owner_access_id, # Todos são owners aqui
                    status=user["status"]
                )
                db.add(new_user)
                print(f"Usuário Root '{user['name']}' criado com sucesso.")
            else:
                print(f"Usuário Root '{user['name']}' já existe.")
        db.commit()

        # Buscar IDs dos usuários root
        ana_id = db.query(UserRootModel.UserRoot.id).filter(UserRootModel.UserRoot.email == "ana@mitescan.com").scalar()
        isabely_id = db.query(UserRootModel.UserRoot.id).filter(UserRootModel.UserRoot.email == "isabely@mitescan.com").scalar()
        gustavo_id = db.query(UserRootModel.UserRoot.id).filter(UserRootModel.UserRoot.email == "gustavo@mitescan.com").scalar()
        yasmin_id = db.query(UserRootModel.UserRoot.id).filter(UserRootModel.UserRoot.email == "yasmin@mitescan.com").scalar()
        
        # --- 3. Usuários Associados (Novo) ---
        associated_users_data = [
            {"name": "Funcionário BeeTech", "email": "employee@beetech.com", "password_hash": get_password_hash("employee123"), "access_id": employee_access_id, "user_root_id": ana_id},
            {"name": "Gerente MiteScan", "email": "manager@mitescan.com", "password_hash": get_password_hash("manager123"), "access_id": manager_access_id, "user_root_id": isabely_id},
        ]

        for user in associated_users_data:
            existing_user = db.query(UserAssociatedModel.UserAssociated).filter(UserAssociatedModel.UserAssociated.email == user["email"]).first()
            
            if not existing_user:
                new_user = UserAssociatedModel.UserAssociated(
                    name=user["name"],
                    email=user["email"],
                    password_hash=user["password_hash"],
                    access_id=user["access_id"], # Usa o ID do loop
                    user_root_id=user["user_root_id"]
                )
                db.add(new_user)
                print(f"Usuário Associado '{user['name']}' criado com sucesso.")
            else:
                print(f"Usuário Associado '{user['name']}' já existe.")

        # --- 4. Tipos de Abelha ---
        bee_types_data = [
            {"name": "Jataí", "description": "A abelha Jataí é uma espécie de abelha sem ferrão..."},
            {"name": "Mandaçaia", "description": "A Mandaçaia é uma abelha sem ferrão..."},
            {"name": "Uruçu", "description": "A Uruçu é uma espécie de abelha sem ferrão..."},
            {"name": "Irapuca", "description": "A Irapuca é uma abelha sem ferrão..."},
        ]
        
        for bee_type in bee_types_data:
            existing_bee_type = db.query(BeeTypeModel.BeeType).filter(BeeTypeModel.BeeType.name == bee_type["name"]).first()
            
            if not existing_bee_type:
                new_bee_type = BeeTypeModel.BeeType(
                    name=bee_type["name"],
                    description=bee_type["description"]
                )
                db.add(new_bee_type)
                print(f"Tipo de abelha '{bee_type['name']}' criado com sucesso.")
            else:
                print(f"Tipo de abelha '{bee_type['name']}' já existe.")
        db.commit()

        # Buscar IDs dos tipos de abelha
        jatai_id = db.query(BeeTypeModel.BeeType.id).filter(BeeTypeModel.BeeType.name == "Jataí").scalar()
        mandacaia_id = db.query(BeeTypeModel.BeeType.id).filter(BeeTypeModel.BeeType.name == "Mandaçaia").scalar()
        urucu_id = db.query(BeeTypeModel.BeeType.id).filter(BeeTypeModel.BeeType.name == "Uruçu").scalar()
        irapuca_id = db.query(BeeTypeModel.BeeType.id).filter(BeeTypeModel.BeeType.name == "Irapuca").scalar()

        # --- 5. Colmeias ---
        hives_data = [
            {"user_root_id": ana_id, "bee_type_id": jatai_id, "location_lat": -23.5505, "location_lng": -46.6333, "size": "Média"},
            {"user_root_id": isabely_id, "bee_type_id": mandacaia_id, "location_lat": -23.5506, "location_lng": -46.6334, "size": "Grande"},
            {"user_root_id": gustavo_id, "bee_type_id": urucu_id, "location_lat": -23.5507, "location_lng": -46.6335, "size": "Pequena"},
            {"user_root_id": yasmin_id, "bee_type_id": irapuca_id, "location_lat": -23.5508, "location_lng": -46.6336, "size": "Média"},
        ]
        
        for hive in hives_data:
            existing_hive = db.query(HiveModel.Hive).filter(HiveModel.Hive.location_lat == hive["location_lat"], HiveModel.Hive.location_lng == hive["location_lng"]).first()
            
            if not existing_hive:
                new_hive = HiveModel.Hive(
                    user_root_id=hive["user_root_id"],
                    bee_type_id=hive["bee_type_id"],
                    location_lat=hive["location_lat"],
                    location_lng=hive["location_lng"],
                    size=hive["size"],
                )
                db.add(new_hive)
                print(f"Colmeia localizada em ({hive['location_lat'], hive['location_lng']}) criada com sucesso.")
            else:
                print(f"Colmeia localizada em ({hive['location_lat'], hive['location_lng']}) já existe.")
        db.commit()

        # Buscar IDs das colmeias
        hive1_id = db.query(HiveModel.Hive.id).filter(HiveModel.Hive.location_lat == -23.5505).scalar()
        hive2_id = db.query(HiveModel.Hive.id).filter(HiveModel.Hive.location_lat == -23.5506).scalar()
        hive3_id = db.query(HiveModel.Hive.id).filter(HiveModel.Hive.location_lat == -23.5507).scalar()
        hive4_id = db.query(HiveModel.Hive.id).filter(HiveModel.Hive.location_lat == -23.5508).scalar()
        
        # --- 6. Leituras de Sensores ---
        sensors_data = [
            {"hive_id": hive1_id, "humidity": 65.0, "temperature": 30.5, "created_at": datetime.utcnow()},
            {"hive_id": hive2_id, "humidity": 66.0, "temperature": 31.5, "created_at": datetime.utcnow()},
            {"hive_id": hive3_id, "humidity": 67.0, "temperature": 32.5, "created_at": datetime.utcnow()},
            {"hive_id": hive4_id, "humidity": 68.0, "temperature": 33.5, "created_at": datetime.utcnow()},
        ]
        
        for sensor in sensors_data:
            existing_sensor = db.query(SensorModel.Sensor).filter(
                SensorModel.Sensor.hive_id == sensor["hive_id"],
                SensorModel.Sensor.created_at == sensor["created_at"]
            ).first()
            
            if not existing_sensor:
                new_sensor = SensorModel.Sensor(
                    hive_id=sensor["hive_id"],
                    humidity=sensor["humidity"],
                    temperature=sensor["temperature"]
                )
                db.add(new_sensor)
                print(f"Leitura do sensor da colmeia {sensor['hive_id']} criada com sucesso.")
            else:
                print(f"Leitura do sensor da colmeia {sensor['hive_id']} já existe.")
        db.commit()

        # --- 7. Análises de Colmeia ---
        analyses_data = [
            {"hive_id": hive1_id, "user_root_id": ana_id, "image_path": "image1.jpg", "varroa_detected": True, "detection_confidence": 0.92, "created_at": datetime.utcnow()},
            {"hive_id": hive2_id, "user_root_id": isabely_id, "image_path": "image2.jpg", "varroa_detected": False, "detection_confidence": 0.98, "created_at": datetime.utcnow()},
            {"hive_id": hive3_id, "user_root_id": gustavo_id, "image_path": "image3.jpg", "varroa_detected": True, "detection_confidence": 0.85, "created_at": datetime.utcnow()},
            {"hive_id": hive4_id, "user_root_id": yasmin_id, "image_path": "image4.jpg", "varroa_detected": False, "detection_confidence": 0.99, "created_at": datetime.utcnow()},
        ]
        
        # Buscar IDs das análises
        analysis1_id = None
        analysis3_id = None

        for analysis in analyses_data: 
            existing_analysis = db.query(AnalysisModel.HiveAnalysis).filter(
                AnalysisModel.HiveAnalysis.hive_id == analysis["hive_id"],
                AnalysisModel.HiveAnalysis.created_at == analysis["created_at"]
            ).first()
            
            if not existing_analysis:
                new_analysis = AnalysisModel.HiveAnalysis(
                    hive_id=analysis["hive_id"],
                    user_root_id=analysis["user_root_id"],
                    image_path=analysis["image_path"],
                    varroa_detected=analysis["varroa_detected"],
                    detection_confidence=analysis["detection_confidence"],
                    created_at=analysis["created_at"]
                )
                db.add(new_analysis)
                print(f"Análise da colmeia '{analysis['hive_id']}' criada com sucesso.")
            else:
                print(f"Análise da colmeia '{analysis['hive_id']}' já existe.")
        db.commit()

        # Buscar IDs das análises para o backup
        analysis1 = db.query(AnalysisModel.HiveAnalysis).filter(AnalysisModel.HiveAnalysis.hive_id == hive1_id).first()
        analysis3 = db.query(AnalysisModel.HiveAnalysis).filter(AnalysisModel.HiveAnalysis.hive_id == hive3_id).first()


        # --- 8. Backups de Análises ---
        backups_data = [
            {"analysis_id": analysis1.id, "user_root_id": ana_id, "file_path": "backup/image1.jpg", "created_at": datetime.utcnow()} if analysis1 else None,
            {"analysis_id": analysis3.id, "user_root_id": gustavo_id, "file_path": "backup/image3.jpg", "created_at": datetime.utcnow()} if analysis3 else None,
        ]

        for backup in backups_data:
            existing_backup = db.query(AnalysisBackupModel.AnalysisBackup).filter(
                AnalysisBackupModel.AnalysisBackup.analysis_id == backup["analysis_id"]
            ).first()

            if not existing_backup:
                new_backup = AnalysisBackupModel.AnalysisBackup(
                    analysis_id=backup["analysis_id"],
                    user_root_id=backup["user_root_id"],
                    file_path=backup["file_path"],
                    created_at=backup["created_at"]
                )
                db.add(new_backup)
                print(f"Backup da análise '{backup['analysis_id']}' criado com sucesso.")
            else:
                print(f"Backup da análise '{backup['analysis_id']}' já existe.")


        print("\nSeed aplicada com sucesso.")
        
    except Exception as e:
        print("\nErro ao aplicar a seed:", e)
        import traceback
        traceback.print_exc()
        db.rollback()
        
    finally:
        try:
            db.close()
        except Exception as e:
            print("Erro ao fechar a sessão do banco de dados: ", e)

if __name__ == "__main__":
    print("Aplicando seed no banco de dados...")
    seed_data()