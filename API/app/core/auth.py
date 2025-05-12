from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session, joinedload
from db.database import SessionLocal, get_db
from core.config import settings
from models.user import User
from models.company import Company
from typing import Type, Union, Optional

secret_key = settings.secret_key
algorithm = settings.algorithm
access_token_expire_minutes = settings.access_token_expire_minutes

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: int = access_token_expire_minutes):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)

def authenticate_entity(entity_type: Type[Union[User, Company]], email: str, password: str, db: Session) -> Optional[Union[User, Company]]:
    entity = db.query(entity_type).filter(entity_type.email == email).first()
    if not entity or not verify_password(password, entity.password_hash):
        return None
    return entity

def authenticate_user(email: str, password: str, db: Session):
    return authenticate_entity(User, email, password, db)

def authenticate_company(email: str, password: str, db: Session):
    return authenticate_entity(Company, email, password, db)

def get_current_entity(entity_type: Type[Union[User, Company]], token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        email: str = payload.get("sub")
        
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        entity = db.query(entity_type).options(joinedload(entity_type.access)).filter(entity_type.email == email).first()
        
        if not entity:
            entity_name = "Usuário" if entity_type == User else "Empresa"
            raise HTTPException(status_code=404, detail=f"{entity_name} não encontrado")
        
        return entity

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return get_current_user(User, token, db)

def get_current_company(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return get_current_company(Company, token, db)

def require_access(*allowed_access):
    def access_checker(user=Depends(get_current_user), company = Depends(get_current_company)):
        if user is not None:
            if user.access.name not in allowed_access:
                raise HTTPException(status_code=403, detail="Acesso negado")
            return user
    
        if company is not None:
            if company.access.name not in allowed_access:
                raise HTTPException(status_code=403, detail="Acesso negado")
            return company
        
        raise HTTPException(status_code=403, detail="Entidade não identificada")
    
    return access_checker
