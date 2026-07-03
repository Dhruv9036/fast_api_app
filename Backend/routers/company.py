from fastapi import APIRouter, HTTPException, Depends, status
from schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse
from models import company, job
from sqlalchemy.orm import Session
from database import get_db
from utils.oauth2 import get_current_user, role_required
router = APIRouter(prefix="/company", tags=["company"])
companies = []

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CompanyResponse
)
def create_company(company_data: CompanyCreate, db: Session = Depends(get_db),current_user=Depends(role_required(["admin"]))):
    print("Reached endpoint")

    db_company = company.Company(
        name=company_data.name,
        email=company_data.email,
        phone=company_data.phone,
        location=company_data.location
    )

    print("Before commit")

    db.add(db_company)
    db.commit()

    print("After commit")

    db.refresh(db_company)

    return db_company

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[CompanyResponse])
def get_all_company(db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    return db.query(company.Company).all()

@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(company_id: int, db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    db_company = (
        db.query(company.Company)
        .filter(company.Company.id == company_id)
        .first()
    )

    if db_company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )

    return db_company

@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(company_id: int, company_data: CompanyUpdate, db: Session = Depends(get_db),current_user=Depends(role_required(["admin"]))):
    db_company = db.query(company.Company).filter(
        company.Company.id == company_id
    ).first()

    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    for key, value in company_data.dict(exclude_unset=True).items():
        setattr(db_company, key, value)

    db.commit()
    db.refresh(db_company)

    return db_company

@router.delete("/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db),current_user=Depends(role_required(["admin"]))):
    db_company = db.query(company.Company).filter(
        company.Company.id == company_id
    ).first()

    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    db.delete(db_company)
    db.commit()

    return {"message": "Company deleted successfully"}
