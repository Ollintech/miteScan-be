from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from db.database import get_db
from API.app.models.users_associated import Company
from schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate
from core.auth import (get_password_hash, authenticate_company, create_access_token, get_current_company)
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime

router = APIRouter(prefix = '/companies', tags = ['Companies'])
pwd_context = CryptContext(schemes = ['bcrypt'], deprecated = ['auto'])

@router.post('/register', response_model = CompanyResponse, status_code = status.HTTP_201_CREATED)
def register_company(company_data: CompanyCreate, db: Session = Depends(get_db)):
    existing_cnpj = db.query(Company).filter(Company.cnpj == company_data.cnpj).first()
    existing_email = db.query(Company).filter(Company.email == company_data.email).first()
    if existing_cnpj:
        raise HTTPException(status_code = 400, detail = "CNPJ já cadastrado.")
    if existing_email:
        raise HTTPException(status_code = 400, detail = "Email já cadastrado.")
    
    new_company = Company(
        name = company_data.name,
        cnpj = company_data.cnpj,
        email = company_data.email,
        password_hash=get_password_hash(company_data.password),
        access_id=company_data.access_id,
        last_login=None
    )

    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company

@router.post('/login')
def login_company(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    company = authenticate_company(email=form_data.username, password=form_data.password, db=db)
    if not company:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    
    company.last_login = datetime.utcnow()
    db.commit()
    
    token_data = {
        "sub": company.email,
        "company_id": company.id,
        "access_id": company.access_id
    }
    
    access_token = create_access_token(data=token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "company": {
            "id": company.id,
            "name": company.name,
            "cnpj": company.cnpj,
            "email": company.email
        }
    }

@router.get('/profile', response_model=CompanyResponse)
def profile_company(current_company: Company = Depends(get_current_company)):
    return current_company

@router.get('/{company_id}', response_model = CompanyResponse)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()

    if not company:
        raise HTTPException(status_code = 404, detail = 'Empresa não encontrada.')
    
    return company

@router.put('/{company_id}', response_model = CompanyResponse)
def update_company(company_id: int, company_update: CompanyUpdate, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()

    if not company:
        raise HTTPException(status_code = 404, detail = 'Empresa não encontrada.')
    
    if company_update.name:
        company.name = company_update.name

    if company_update.cnpj:
        if db.query(Company).filter(Company.cnpj == company_update.cnpj).first():
            raise HTTPException(status_code = 400, detail = 'CNPJ já cadastrado.')
        company.cnpj = company_update.cnpj
        
    if company_update.email and company_update.email != company.email:
        if db.query(Company).filter(Company.email == company_update.email).first():
            raise HTTPException(status_code=400, detail="Email já cadastrado.")
        company.email = company_update.email

    if company_update.password:
        company.password_hash = get_password_hash(company_update.password)

    if company_update.access_id:
        company.access_id = company_update.access_id

    db.commit()
    db.refresh(company)

    return company

@router.delete('/{company_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(status_code = 404, detail = 'Empresa não encontrada.')
    
    db.delete(company)
    db.commit()

    return {'message': 'Empresa deletada com sucesso!'}