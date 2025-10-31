from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from db.database import get_db
from core.auth import (
    authenticate_user_root,
    authenticate_user_associated,
    create_access_token
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login/root")
def login_user_root(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint de login para Usuários Root.
    """
    user_root = authenticate_user_root(email=form_data.username, password=form_data.password, db=db)
    if not user_root:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    if not user_root.status:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário inativo")

    user_root.last_login = datetime.now(timezone.utc)
    db.commit()

    token_data = {
        "sub": user_root.email,
        "account": user_root.account,
        "access_id": user_root.access_id
    }
    access_token = create_access_token(data=token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user_root.id,
            "name": user_root.name,
            "email": user_root.email,
            "account": user_root.account,
            "status": user_root.status,
            "access_id": user_root.access_id,
            "role": "root"
        }
    }


@router.post("/login/associated")
def login_user_associated(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint de login para Usuários Associados.
    """
    user_associated = authenticate_user_associated(
        email=form_data.username, password=form_data.password, db=db)
    
    if not user_associated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    if not user_associated.status:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário inativo")

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
        "user": { 
            "id": user_associated.id,
            "name": user_associated.name,
            "email": user_associated.email,
            "account": user_associated.account,
            "status": user_associated.status,
            "role": "associated" 
        }
    }