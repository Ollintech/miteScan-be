from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from db.database import get_db
from models.user_associated import UserAssociated
from models.user_root import UserRoot
from schemas.user_associated import UserAssociatedCreate, UserAssociatedResponse, UserAssociatedUpdate
from core.exceptions import DuplicateEntryError, ResourceNotFoundError
from core.auth import (get_password_hash, get_current_user_associated, get_current_user_root)
from typing import List


router = APIRouter(
    prefix='/{account}/users_associated', tags=['Users Associated'])


def check_root_permission(account: str, current_user_root: UserRoot):
    """Função helper para verificar se o root logado é o mesmo da URL"""
    if not current_user_root:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Não autenticado como usuário root")
    if current_user_root.account != account:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Acesso negado para este recurso")
        

@router.post('/register', response_model = UserAssociatedResponse, status_code = status.HTTP_201_CREATED)
def register_user_associated(
    account: str,
    user_associated_data: UserAssociatedCreate, 
    db: Session = Depends(get_db),
    current_user_root: UserRoot = Depends(get_current_user_root)
):
    """
    PROTEGIDO: Apenas o UserRoot correspondente pode registrar.
    """
    check_root_permission(account, current_user_root)
    
    existing_email = db.query(UserAssociated).filter(UserAssociated.email == user_associated_data.email).first()
    if existing_email:
        raise DuplicateEntryError("Email")
    
    new_user_associated = UserAssociated(
        name = user_associated_data.name,
        email = user_associated_data.email,
        account = account,
        password_hash=get_password_hash(user_associated_data.password),
        access_id=user_associated_data.access_id,
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
    account: str,
    db: Session = Depends(get_db),
    current_user_root: UserRoot = Depends(get_current_user_root)
):
    """
    PROTEGIDO: Lista todos os usuários associados daquele root.
    """
    check_root_permission(account, current_user_root)
    
    users = db.query(UserAssociated).filter(UserAssociated.account == account).all()
    return users


@router.get('/{user_associated_id}', response_model = UserAssociatedResponse)
def get_user_associated(
    account: str,
    user_associated_id: int, 
    db: Session = Depends(get_db),
    current_user_root: UserRoot = Depends(get_current_user_root)
):
    """
    PROTEGIDO: Apenas o UserRoot pode ver usuários associados específicos.
    """
    check_root_permission(account, current_user_root)

    user_associated = db.query(UserAssociated).filter(
        UserAssociated.id == user_associated_id,
        UserAssociated.account == account
    ).first()

    if not user_associated:
        raise ResourceNotFoundError('Usuário Associado')
    
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
    user_to_update = current_user_associated
    
    update_data = user_associated_update.model_dump(exclude_unset=True)
        
    if 'email' in update_data and update_data['email'] != user_to_update.email:
        if db.query(UserAssociated).filter(UserAssociated.email == update_data['email']).first():
            raise HTTPException(status_code=400, detail="Email já cadastrado.")

    if 'password' in update_data:
        update_data['password_hash'] = get_password_hash(update_data.pop('password'))

    for key, value in update_data.items():
        setattr(user_to_update, key, value)
    
    db.commit()
    db.refresh(user_to_update)

    return user_to_update


@router.put('/{user_associated_id}', response_model = UserAssociatedResponse)
def update_user_associated(
    account: str,
    user_associated_id: int, 
    user_associated_update: UserAssociatedUpdate, 
    db: Session = Depends(get_db),
    current_user_root: UserRoot = Depends(get_current_user_root)
):
    """
    PROTEGIDO: Apenas o UserRoot pode editar outros usuários.
    """
    check_root_permission(account, current_user_root)

    user_associated = db.query(UserAssociated).filter(
        UserAssociated.id == user_associated_id,
        UserAssociated.account == account
    ).first()

    if not user_associated:
        raise HTTPException(status_code = 404, detail = 'Usuário Associado não encontrado.')
    
    update_data = user_associated_update.model_dump(exclude_unset=True)
        
    if 'email' in update_data and update_data['email'] != user_associated.email:
        if db.query(UserAssociated).filter(UserAssociated.email == update_data['email']).first():
            raise HTTPException(status_code=400, detail="Email já cadastrado.")

    if 'password' in update_data:
        update_data['password_hash'] = get_password_hash(update_data.pop('password'))

    for key, value in update_data.items():
        setattr(user_associated, key, value)

    db.commit()
    db.refresh(user_associated)

    return user_associated


@router.delete('/{user_associated_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_user_associated(
    account: str,
    user_associated_id: int, 
    db: Session = Depends(get_db),
    current_user_root: UserRoot = Depends(get_current_user_root)
):
    """
    PROTEGIDO: Apenas o UserRoot pode deletar usuários.
    """
    
    user_associated = db.query(UserAssociated).filter(
        UserAssociated.id == user_associated_id,
        UserAssociated.account == account
    ).first()
    
    if not user_associated:
        raise HTTPException(status_code = 404, detail = 'Usuário Associado não encontrado.')
    
    db.delete(user_associated)
    db.commit()
    
    return None