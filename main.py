from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal, User
from auth import get_password_hash, authenticate_user, create_access_token, get_current_user, get_db

app = FastAPI()

@app.post("/register")
def register(name: str, email: str, password: str, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    hashed_password = get_password_hash(password)
    new_user = User(name=name, email=email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "Usuário registrado com sucesso"}

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/users/me")
def get_current_user_info(user: User = Depends(get_current_user)):
    return {"name": user.name, "email": user.email}
