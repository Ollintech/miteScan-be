from sqlalchemy.orm import Session
from db.database import SessionLocal
from models import company as CompanyModel
from models import user as UserModel
from models import access as AccessModel
from models import bee_type as BeeTypeModel
from models import hive as HiveModel
from models import hive_analysis as AnalysisModel
from datetime import datetime
from core.auth import get_password_hash

def seed_data():
    db: Session = SessionLocal()
    try:

        access = db.query(AccessModel.Access).filter(AccessModel.Access.name == "owner").first()
        if not access:
            access = AccessModel.Access(name="owner", description="General administrator")
            db.add(access)
            db.commit()
            db.refresh(access)
        else:
            print("O nível de acesso 'owner' já existe.")

        company = db.query(CompanyModel.Company).filter(CompanyModel.Company.cnpj == "12345678901234").first()
        if not company:
            company = CompanyModel.Company(name="BeeTech", cnpj="12345678901234")
            db.add(company)
            db.commit()
            db.refresh(company)
        else:
            print(f"Empresa {company.name} já existe.")

        user = db.query(UserModel.User).filter(UserModel.User.email == "ana@example.com").first()
        if not user:
            user = UserModel.User(
                name="Ana",
                email="ana@example.com",
                password_hash=get_password_hash("12345678"),
                access_id=access.id,
                company_id=company.id,
                status=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            print(f"Usuário {user.name} já existe.")

        bee_type = db.query(BeeTypeModel.BeeType).filter(BeeTypeModel.BeeType.name == "Apis mellifera").first()
        if not bee_type:
            bee_type = BeeTypeModel.BeeType(
                name="Apis mellifera",
                description="European bee",
                user_id=user.id
            )
            db.add(bee_type)
            db.commit()
            db.refresh(bee_type)
        else:
            print(f"O tipo de abelha {bee_type.name} já existe.")


        hive = db.query(HiveModel.Hive).filter(HiveModel.Hive.user_id == user.id, HiveModel.Hive.bee_type_id == bee_type.id).first()
        if not hive:
            hive = HiveModel.Hive(
                user_id=user.id,
                bee_type_id=bee_type.id,
                location_lat=-23.5505,
                location_lng=-46.6333,
                size=10,
                humidity=65.0,
                temperature=30.5
            )
            db.add(hive)
            db.commit()
            db.refresh(hive)
        else:
            print("Essa colmeia já existe.")

        analysis = db.query(AnalysisModel.HiveAnalysis).filter(AnalysisModel.HiveAnalysis.hive_id == hive.id).first()
        if not analysis:
            analysis = AnalysisModel.HiveAnalysis(
                hive_id=hive.id,
                user_id=user.id,
                image_path="image.jpg",
                varroa_detected=True,
                detection_confidence=0.92,
                created_at=datetime.utcnow()
            )
            db.add(analysis)
            db.commit()
            db.refresh(analysis)
        else:
            print("Essa análise já existe.")

        print("Seed aplicada com sucesso.")
    except Exception as e:
        print("Erro ao aplicar a seed:", e)
    finally:
        db.close()
