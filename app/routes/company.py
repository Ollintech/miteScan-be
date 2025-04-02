from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from db.database import get_db
from models.company import Company
from schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate

router = APIRouter(prefix = '/companies', tags = ['companies'])

pwd_context = CryptContext(schemes = ['bcrypt'], deprecated = ['auto'])

# Rota de criação de empresa
@router.post('/create', response_model = CompanyResponse, status_code = status.HTTP_201_CREATED)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    if db.query(Company).filter(Company.cnpj == company.cnpj).first():
        raise HTTPException(status_code = 400, detail = "CNPJ já cadastrado.")
    
    new_company = Company(
        name = company.name,
        cnpj = company.cnpj,
    )

    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company

# Rota para obter os dados da empresa
@router.get('/get:{company_id}', response_model = CompanyResponse)
def get_user(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()

    if not company:
        raise HTTPException(status_code = 404, detail = 'Empresa não encontrada.')
    
    return company

# Rota para atualizar os dados da empresa
@router.put('/put:{company_id}', response_model = CompanyResponse)
def update_company(company_id: int, company_update: CompanyResponse, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()

    if not company:
        raise HTTPException(status_code = 404, detail = 'Empresa não encontrada.')
    
    if company_update.name:
        company.name = company_update.name

    if company_update.cnpj:
        if db.query(Company).filter(Company.cnpj == company_update.cnpj).first():
            raise HTTPException(status_code = 400, detail = 'CNPJ já cadastrado.')
        company.cnpj = company_update.cnpj

    db.commit()
    db.refresh(company)

    return company

# Rota para deletar uma empresa
@router.delete('/delete:{company_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_user(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(status_code = 404, detail = 'Empresa não encontrada.')
    
    db.delete(company)
    db.commit()

    return {'message': 'Empresa deletada com sucesso!'}