from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from db.database import get_db
from models.access import Access
from schemas.access import AccessResponse

router = APIRouter(prefix = '/access', tags = ['accesss'])

# Rota para obter os dados de acesso
@router.get('/get:{access_id}', response_model = AccessResponse)
def get_access(access_id: int, db: Session = Depends(get_db)):
    access = db.query(Access).filter(Access.id == access_id).first()

    if not access:
        raise HTTPException(status_code = 404, detail = 'Acesso não encontrado.')

    return access

 