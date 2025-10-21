from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from db.database import get_db
from models.users_associated import UserAssociated
from models.user_root import UserRoot
from schemas.user_associated import UserAssociatedCreate, UserAssociatedResponse, UserAssociatedUpdate
from core.auth import (get_password_hash, authenticate_user_associated, create_access_token, get_current_user_associated)
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timezone

router = APIRouter(prefix = '/{user_root_id}/users_associated', tags = ['Users Associated'])
pwd_context = CryptContext(schemes = ['bcrypt'], deprecated = ['auto'])

@router.post('/register', response_model = UserAssociatedResponse, status_code = status.HTTP_201_CREATED)
def register_user_associated(user_associated_data: UserAssociatedCreate, db: Session = Depends(get_db)):
    existing_email = db.query(UserAssociated).filter(UserAssociated.email == user_associated_data.email).first()
    if existing_email:
        raise HTTPException(status_code = 400, detail = "Email já cadastrado.")
    
    new_user_associated = UserAssociated(
        name = user_associated_data.name,
        email = user_associated_data.email,
        password_hash=get_password_hash(user_associated_data.password),
        access_id=user_associated_data.access_id,
        user_id=user_associated_data.user_id,
        last_login=None
    )

    db.add(new_user_associated)
    db.commit()
    db.refresh(new_user_associated)

    return new_user_associated

@router.post('/login')
def login_user_associated(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_associated = authenticate_user_associated(email=form_data.username, password=form_data.password, db=db)
    if not user_associated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    user_associated.last_login = datetime.now(timezone.utc)
    db.commit()
    
    token_data = {
        "sub": user_associated.email,
        "user_associated_id": user_associated.id,
        "access_id": user_associated.access_id
    }
    
    access_token = create_access_token(data=token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_associated": {
            "id": user_associated.id,
            "name": user_associated.name,
            "email": user_associated.email
        }
    }

@router.get('/profile', response_model=UserAssociatedResponse)
def profile_user_associated(current_user_associated: UserAssociated = Depends(get_current_user_associated)):
    return current_user_associated

@router.get('/{user_associated_id}', response_model = UserAssociatedResponse)
def get_user_associated(user_associated_id: int, db: Session = Depends(get_db)):
    user_associated = db.query(UserAssociated).filter(UserAssociated.id == user_associated_id).first()

    if not user_associated:
        raise HTTPException(status_code = 404, detail = 'Usuário Associado não encontrado.')
    
    return user_associated

@router.put('/{user_associated_id}', response_model = UserAssociatedResponse)
def update_user_associated(user_associated_id: int, user_associated_update: UserAssociatedUpdate, db: Session = Depends(get_db)):
    user_associated = db.query(UserAssociated).filter(UserAssociated.id == user_associated_id).first()

    if not user_associated:
        raise HTTPException(status_code = 404, detail = 'Usuário Associado não encontrado.')
    
    if user_associated_update.name:
        user_associated.name = user_associated_update.name
        
    if user_associated_update.email and user_associated_update.email != user_associated.email:
        if db.query(UserAssociated).filter(UserAssociated.email == user_associated_update.email).first():
            raise HTTPException(status_code=400, detail="Email já cadastrado.")
        user_associated.email = user_associated_update.email

    if user_associated_update.password:
        user_associated.password_hash = get_password_hash(user_associated_update.password)

    if user_associated_update.access_id:
        user_associated.access_id = user_associated_update.access_id

    db.commit()
    db.refresh(user_associated)

    return user_associated

@router.delete('/{user_associated_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_user_associated(user_associated_id: int, db: Session = Depends(get_db)):
    user_associated = db.query(UserAssociated).filter(UserAssociated.id == user_associated_id).first()
    
    if not user_associated:
        raise HTTPException(status_code = 404, detail = 'Usuário Associado não encontrado.')
    
    db.delete(user_associated)
    db.commit()

    return {'message': 'Usuário Associado deletada com sucesso!'}