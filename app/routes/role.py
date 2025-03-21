from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from db.database import get_db
from models.role import Role
from schemas.role import RoleResponse

router = APIRouter(prefix = '/role', tags = ['roles'])

# Rota para obter os dados de acesso
@router.get('/get:{role_id}', response_model = RoleResponse)
def get_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(status_code = 404, detail = 'Acesso não encontrado.')

    return role

 