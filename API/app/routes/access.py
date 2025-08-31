from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from db.database import get_db
from models.access import Access
from schemas.access import AccessResponse

router = APIRouter(prefix = '/accesses', tags = ['Accesses'])

@router.get('/all', response_model = list[AccessResponse])
def get_all_accesses(db: Session = Depends(get_db)):
    accesses = db.query(Access).all()

    if not accesses:
        raise HTTPException(status_code = 404, detail = 'Não existe nenhum acesso cadastrado.')

    return accesses

@router.get('/{access_id}', response_model = AccessResponse)
def get_access(access_id: int, db: Session = Depends(get_db)):
    access = db.query(Access).filter(Access.id == access_id).first()

    if not access:
        raise HTTPException(status_code = 404, detail = 'Acesso não encontrado.')

    return access

 