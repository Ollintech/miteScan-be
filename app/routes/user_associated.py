from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from db.database import get_db
from models.users_associated import UserAssociated
from models.user_root import UserRoot
from schemas.user_associated import UserAssociatedCreate, UserAssociatedResponse, UserAssociatedUpdate
from core.auth import (get_password_hash, authenticate_user_associated,
                       create_access_token, get_current_user_associated, get_current_user_root)
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timezone
from typing import List


router = APIRouter(
    prefix='/{user_root_id}/users_associated', tags=['Users Associated'])
pwd_context = CryptContext(schemes=['bcrypt'], deprecated=['auto'])


def check_root_permission(user_root_id: int, current_user_root: UserRoot):
    """Função helper para verificar se o root logado é o mesmo da URL"""
    if not current_user_root:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Não autenticado como usuário root")
    if current_user_root.id != user_root_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Acesso negado para este recurso")
        

@router.post('/register', response_model = UserAssociatedResponse, status_code = status.HTTP_201_CREATED)
def register_user_associated(
    user_root_id: int,
    user_associated_data: UserAssociatedCreate, 
    db: Session = Depends(get_db),
    current_user_root: UserRoot = Depends(get_current_user_root)
):
    """
    PROTEGIDO: Apenas o UserRoot correspondente pode registrar.
    """
    check_root_permission(user_root_id, current_user_root)
    
    existing_email = db.query(UserAssociated).filter(UserAssociated.email == user_associated_data.email).first()
    if existing_email:
        raise HTTPException(status_code = 400, detail = "Email já cadastrado.")
    
    new_user_associated = UserAssociated(
        name = user_associated_data.name,
        email = user_associated_data.email,
        password_hash=get_password_hash(user_associated_data.password),
        access_id=user_associated_data.access_id,
        user_root_id = user_root_id,
        last_login=None
    )

    db.add(new_user_associated)
    db.commit()
    db.refresh(new_user_associated)

    return new_user_associated


@router.get('/profile', response_model=UserAssociatedResponse)
def profile_user_associated(current_user_associated: UserAssociated = Depends(get_current_user_associated)):
    """
    Permite que o USUÁRIO ASSOCIADO logado veja seu próprio perfil.
    """
    return current_user_associated


@router.get('/', response_model=List[UserAssociatedResponse])
def list_users_associated(
    user_root_id: int,
    db: Session = Depends(get_db),
    current_user_root: UserRoot = Depends(get_current_user_root)
):
    """
    PROTEGIDO: Lista todos os usuários associados daquele root.
    """
    check_root_permission(user_root_id, current_user_root)
    
    users = db.query(UserAssociated).filter(UserAssociated.user_root_id == user_root_id).all()
    return users


@router.get('/{user_associated_id}', response_model = UserAssociatedResponse)
def get_user_associated(
    user_root_id: int,
    user_associated_id: int, 
    db: Session = Depends(get_db),
    current_user_root: UserRoot = Depends(get_current_user_root)
):
    """
    PROTEGIDO: Apenas o UserRoot pode ver usuários associados específicos.
    """
    check_root_permission(user_root_id, current_user_root)

    user_associated = db.query(UserAssociated).filter(
        UserAssociated.id == user_associated_id,
        UserAssociated.user_root_id == user_root_id
    ).first()

    if not user_associated:
        raise HTTPException(status_code = 404, detail = 'Usuário Associado não encontrado.')
    
    return user_associated


@router.put('/profile', response_model=UserAssociatedResponse)
def update_own_profile(
    user_associated_update: UserAssociatedUpdate, 
    db: Session = Depends(get_db), 
    current_user_associated: UserAssociated = Depends(get_current_user_associated)
):
    """
    Permite que o USUÁRIO ASSOCIADO logado atualize seu próprio perfil.
    """
    user_associated = current_user_associated
    
    if user_associated_update.name:
        user_associated.name = user_associated_update.name
        
    if user_associated_update.email and user_associated_update.email != user_associated.email:
        if db.query(UserAssociated).filter(UserAssociated.email == user_associated_update.email).first():
            raise HTTPException(status_code=400, detail="Email já cadastrado.")
        user_associated.email = user_associated_update.email

    if user_associated_update.password:
        user_associated.password_hash = get_password_hash(user_associated_update.password)
    
    db.commit()
    db.refresh(user_associated)

    return user_associated


@router.put('/{user_associated_id}', response_model = UserAssociatedResponse)
def update_user_associated(
    user_root_id: int,
    user_associated_id: int, 
    user_associated_update: UserAssociatedUpdate, 
    db: Session = Depends(get_db),
    current_user_root: UserRoot = Depends(get_current_user_root)
):
    """
    PROTEGIDO: Apenas o UserRoot pode editar outros usuários.
    """
    check_root_permission(user_root_id, current_user_root)

    user_associated = db.query(UserAssociated).filter(
        UserAssociated.id == user_associated_id,
        UserAssociated.user_root_id == user_root_id
    ).first()

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
def delete_user_associated(
    user_root_id: int,
    user_associated_id: int, 
    db: Session = Depends(get_db),
    current_user_root: UserRoot = Depends(get_current_user_root)
):
    """
    PROTEGIDO: Apenas o UserRoot pode deletar usuários.
    """
    check_root_permission(user_root_id, current_user_root) 
    
    user_associated = db.query(UserAssociated).filter(
        UserAssociated.id == user_associated_id,
        UserAssociated.user_root_id == user_root_id
    ).first()
    
    if not user_associated:
        raise HTTPException(status_code = 404, detail = 'Usuário Associado não encontrado.')
    
    db.delete(user_associated)
    db.commit()

    return None