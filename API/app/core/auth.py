from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from db.database import SessionLocal
import secrets
from core.config import settings
from sqlalchemy.orm import joinedload
from models.user import User

strong_secret = secrets.token_urlsafe(64)
secret_key = strong_secret
algorithm = settings.algorithm
access_token_expire_minutes = settings.access_token_expire_minutes

pwd_context = CryptContext(schemes = ['pbkdf2_sha256'], deprecated = 'auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'token')

def create_access_token(data: dict, expires_delta: int = access_token_expire_minutes):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = expires_delta)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, secret_key, algorithm = algorithm)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        email: str = payload.get("sub")

        user = db.query(User).options(joinedload(User.access)).filter(User.email == email).first()

        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

def require_access(*allowed_access):
    def access_checker(user = Depends(get_current_user)):
        if user.access.name not in allowed_access:
            raise HTTPException(status_code=403, detail="Acesso negado")
        return user
    return access_checker
