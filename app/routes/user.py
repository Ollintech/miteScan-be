from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime
from db.database import get_db
from models.user import User
from schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix = '/users', tags = ['users'])

pwd_context = CryptContext(schemes = ['bcrypt'], deprecated = ['auto'])

def get_password_hash(password: str):
    return pwd_context.hash(password)

# Rota de criação do usuário
@router.post('/create', response_model = UserResponse, status_code = status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code = 400, detail = "Email já cadastrado.")
    
    new_user = User(
        name = user.name,
        email = user.email,
        password_hash = get_password_hash(user.password),
        status = False,
        last_login = None,
        role_id = user.role_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# Rota para obter os dados do usuário
@router.get('/get:{user_id}', response_model = UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code = 404, detail = 'Usuário não encontrado.')
    
    return user

# Rota para atualizar os dados do usuário
@router.put('/put:{user_id}', response_model = UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code = 404, detail = 'Usuário não encontrado.')
    
    if user_update.name:
        user.name = user_update.name

    if user_update.email:
        if db.query(User).filter(User.email == user_update.email).first():
            raise HTTPException(status_code = 400, detail = 'Email já cadastrado.')
        user.email = user_update.email

    if user_update.password:
        user.password_hash = get_password_hash(user_update.password)

    if user_update.status is not None:
        user.status = user_update.status

    db.commit()
    db.refresh(user)

    return user

# Rota para deletar um usuário
@router.delete('/delete:{user_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code = 404, detail = 'Usuário não encontrado.')
    
    db.delete(user)
    db.commit()

    return {'message': 'Usuário deletado com sucesso!'}