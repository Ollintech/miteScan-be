from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal, User

secret_key = ''
algorithm = 'HS256'
access_token_expire_minutes = 30

pwd_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')

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
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
