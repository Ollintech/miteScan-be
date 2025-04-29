from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime
from db.database import get_db
from models.user import User
from schemas.user import UserCreate, UserResponse, UserUpdate
from core.auth import (
    get_password_hash,
    create_access_token,
    authenticate_user,
    verify_password
)

router = APIRouter(prefix="/users", tags=["Users"])

# ========== Registro ==========

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        access_id=user_data.access_id,
        company_id=user_data.company_id,
        status=False,
        last_login=None
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# ========== Login ==========

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    if not user.status:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário inativo")

    user.last_login = datetime.utcnow()
    db.commit()

    token_data = {
        "sub": user.email,
        "user_id": user.id,
        "access_id": user.access_id
    }

    access_token = create_access_token(data=token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "status": user.status
        }
    }

# ========== CRUD ==========

@router.post("/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar se o email já está cadastrado
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    
    # Criar um novo usuário
    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=get_password_hash(user.password),
        status=False,
        last_login=None,
        access_id=user.access_id,
        company_id=user.company_id
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    if user_update.name:
        user.name = user_update.name

    if user_update.email and user_update.email != user.email:
        if db.query(User).filter(User.email == user_update.email).first():
            raise HTTPException(status_code=400, detail="Email já cadastrado.")
        user.email = user_update.email

    if user_update.password:
        user.password_hash = get_password_hash(user_update.password)

    if user_update.status is not None:
        user.status = user_update.status

    if user_update.access_id:
        user.access_id = user_update.access_id

    if user_update.company_id:
        user.company_id = user_update.company_id

    db.commit()
    db.refresh(user)

    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    db.delete(user)
    db.commit()

    return {"message": "Usuário deletado com sucesso!"}
