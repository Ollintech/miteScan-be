from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime
from db.database import get_db
from models.role import Role
from schemas.role import RoleResponse, RoleUpdate

router = APIRouter(prefix = '/role', tags = ['roles'])

pwd_context = CryptContext(schemes = ['bcrypt'], deprecated = ['auto'])

@router.get('/{role_id}', response_model = RoleResponse)
def get_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(status_code = 404, detail = 'Acesso não encontrado.')

    return role

 