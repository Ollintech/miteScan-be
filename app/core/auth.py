from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session, joinedload
from db.database import get_db
from core.config import settings
from models.user_root import UserRoot
from models.user_associated import UserAssociated
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
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def authenticate_entity(entity_type: Type[Union[UserRoot, UserAssociated]], email: str, password: str, db: Session) -> Optional[Union[UserRoot, UserAssociated]]:
    entity = db.query(entity_type).filter(entity_type.email == email).first()
    if not entity or not verify_password(password, entity.password_hash):
        return None
    return entity


def authenticate_user_root(email: str, password: str, db: Session):
    return authenticate_entity(UserRoot, email, password, db)


def authenticate_user_associated(email: str, password: str, db: Session):
    return authenticate_entity(UserAssociated, email, password, db)


def get_current_entity(entity_type: Type[Union[UserRoot, UserAssociated]], token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        email: str = payload.get("sub")
        
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        entity = db.query(entity_type).options(joinedload(entity_type.access)).filter(entity_type.email == email).first()
        
        if not entity:
            entity_name = "Usuário Raíz" if entity_type == UserRoot else "Usuário Associado"
            raise HTTPException(status_code=404, detail=f"{entity_name} não encontrado")
        
        return entity

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
    

def get_current_user_root(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return get_current_entity(UserRoot, token, db)


def get_current_user_associated(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return get_current_entity(UserAssociated, token, db)


def require_access(*allowed_access):
    def access_checker(user_root=Depends(get_current_user_root), user_associated = Depends(get_current_user_associated)):
        if user_root is not None:
            if user_root.access.name not in allowed_access:
                raise HTTPException(status_code=403, detail="Acesso negado")
            return user_root
    
        if user_associated is not None:
            if user_associated.access.name not in allowed_access:
                raise HTTPException(status_code=403, detail="Acesso negado")
            return user_associated
        
        raise HTTPException(status_code=403, detail="Entidade não identificada")
    
    return access_checker


def get_current_entity_optional(
    entity_type: Type[Union[UserRoot, UserAssociated]], 
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> Optional[Union[UserRoot, UserAssociated]]:
    """
    Versão opcional do 'get_current_entity'.
    Retorna None em vez de HTTPException em caso de erro.
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        email: str = payload.get("sub")
        
        if email is None:
            return None

        entity = db.query(entity_type).options(joinedload(entity_type.access)).filter(entity_type.email == email).first()
        
        if not entity:
            return None
        
        return entity

    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, HTTPException):
        return None
    

def get_current_user_root_optional(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> Optional[UserRoot]:
    """Dependência opcional para o UserRoot."""
    return get_current_entity_optional(UserRoot, token, db)


def get_current_user_associated_optional(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> Optional[UserAssociated]:
    """Dependência opcional para o UserAssociated."""
    return get_current_entity_optional(UserAssociated, token, db)