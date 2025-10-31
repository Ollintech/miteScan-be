from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from db.database import get_db
from models.user_root import UserRoot
from schemas.user_root import UserRootCreate, UserRootResponse, UserRootUpdate
from models.hive import Hive
from models.hive_analysis import HiveAnalysis
from models.sensor_readings import Sensor
from models.user_associated import UserAssociated
from schemas.user_associated import UserAssociatedResponse
from core.auth import (
    get_password_hash,
    create_access_token,
    authenticate_user_root,
    get_current_user_root
)

router = APIRouter(prefix="/users_root", tags=["Users Root"])

@router.post("/register", response_model=UserRootResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRootCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserRoot).filter(UserRoot.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    new_user_root = UserRoot(
        name=user_data.name,
        email=user_data.email,
        account = user_data.account,
        password_hash=get_password_hash(user_data.password),
        access_id=user_data.access_id,
        status=True,
        last_login=None
    )

    db.add(new_user_root)
    db.commit()
    db.refresh(new_user_root)

    return new_user_root

    
@router.get("/profile", response_model = UserRootResponse)
def profile_user(current_user: UserRoot = Depends(get_current_user_root)):
    return current_user

@router.get("/{account}", response_model=UserRootResponse)
def get_user_root(account: str, db: Session = Depends(get_db)):
    user_root = db.query(UserRoot).filter(UserRoot.account == account).first()
    if not user_root:
        raise HTTPException(status_code=404, detail="Usuário Raiz não encontrado.")
    return user_root

@router.get('/{account}/users_associated', response_model = UserAssociatedResponse)
def get_all_users_associated(account: str, db: Session = Depends(get_db)):
    users_associated = db.query(UserAssociated).filter(UserRoot.account == account).all()

    if not users_associated:
        raise HTTPException(status_code = 404, detail = 'Usuários Associados não encontrados.')
    
    return users_associated

@router.put("/{account}", response_model=UserRootResponse)
def update_user_root(account: str, user_root_update: UserRootUpdate, db: Session = Depends(get_db)):
    user_root = db.query(UserRoot).filter(UserRoot.account == account).first()
    if not user_root:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    if user_root_update.name:
        user_root.name = user_root_update.name

    if user_root_update.email and user_root_update.email != user_root.email:
        if db.query(UserRoot).filter(UserRoot.email == user_root_update.email).first():
            raise HTTPException(status_code=400, detail="Email já cadastrado.")
        user_root.email = user_root_update.email

    if user_root_update.account and user_root_update.account != user_root.account:
        if db.query(UserRoot).filter(UserRoot.account == user_root_update.account).first():
            raise HTTPException(status_code=400, detail="Conta já cadastrada.")
        user_root.account = user_root_update.account

    if user_root_update.password:
        user_root.password_hash = get_password_hash(user_root_update.password)

    if user_root_update.status is not None:
        user_root.status = user_root_update.status

    if user_root_update.access_id:
        user_root.access_id = user_root_update.access_id

    db.commit()
    db.refresh(user_root)

    return user_root

@router.delete("/{account}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_root(account: str, db: Session = Depends(get_db)):
    user_root = db.query(UserRoot).filter(UserRoot.account == account).first()
    if not user_root:
        raise HTTPException(status_code=404, detail="Usuário Raiz não encontrado.")

    try:
        hives = db.query(Hive).filter(Hive.account == account).all()
        for hive in hives:
            db.query(HiveAnalysis).filter(HiveAnalysis.hive_id == hive.id).delete(synchronize_session=False)
            db.query(Sensor).filter(Sensor.hive_id == hive.id).delete(synchronize_session=False)
            db.delete(hive)

        db.query(UserAssociated).filter(UserAssociated.account == account).delete(synchronize_session=False)
        
        db.delete(user_root)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar usuário e seus dados: {e}")

    return None
