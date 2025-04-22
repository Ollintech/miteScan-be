from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from models.bee_type import BeeType
from schemas.bee_type import BeeTypeCreate, BeeTypeResponse, BeeTypeUpdate

router = APIRouter(prefix = '/bee_types', tags = ['Bee Types'])

# Rota de criação de tipo de abelha
@router.post('/create', response_model = BeeTypeResponse, status_code = status.HTTP_201_CREATED)
def create_bee_type(bee_type: BeeTypeCreate, db: Session = Depends(get_db)):
    if db.query(BeeType).filter(BeeType.name == bee_type.name).first():
        raise HTTPException(status_code = 400, detail = 'Abelha já cadastrada.')
    
    new_bee_type = BeeType(
        name = bee_type.name,
        description = bee_type.description,
        user_id = bee_type.user_id
    )

    db.add(new_bee_type)
    db.commit()
    db.refresh(new_bee_type)

    return new_bee_type

# Rota que retorna os dados do tipo de abelha
@router.get('/{bee_type_id}', response_model = BeeTypeResponse)
def get_bee_type(bee_type_id: int, db: Session = Depends(get_db)):
    bee_type = db.query(BeeType).filter(BeeType.id == bee_type_id).first()

    if not bee_type:
        raise HTTPException(status_code = 404, detail = 'Abelha não encontrada.')
    
    return bee_type

# Rota para atualizar um tipo de abelha ja existente
@router.put('/{bee_type_id}', response_model = BeeTypeResponse)
def update_bee_type(bee_type_id: int, bee_type_update: BeeTypeUpdate, db: Session = Depends(get_db)):
    bee_type = db.query(BeeType).filter(BeeType.id == bee_type_id).fisrt()

    if not bee_type:
        raise HTTPException(status_code = 404, detail = 'Abelha não encontrada.')

    if bee_type_update.name:
        bee_type.name = bee_type_update.name

    if bee_type_update.description:
        bee_type.description = bee_type_update.description

    db.commit()
    db.refresh(bee_type)

    return bee_type

# Rota para deletar um tipo de abelha
@router.delete('/{bee_type_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_bee_type(bee_type_id: int, db: Session = Depends(get_db)):
    bee_type = db.query(BeeType).filter(BeeType.id == bee_type_id).first()

    if not bee_type:
        raise HTTPException(status_code = 404, detail = 'Abelha não encontrada.')

    db.delete(bee_type)
    db.commit()

    return {'message': 'Tipo de abelha deletado com sucesso!'}