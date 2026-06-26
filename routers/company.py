from fastapi import APIRouter
from schemas.company import CompanyCreate,CompanyUpdate

router = APIRouter(prefix="/company", tags=["company"])
companies = []

@router.post("/")
def create_company(company: CompanyCreate):
    companies.append(company)
    return company

@router.get("/")
def get_all_company():
    return companies


# @router.get("/")
# def read_company():
#     return {"Company": "Company Root"}

# @router.get("/id")
# def read_company_id():
#     return {"Company ID": "12345"}

@router.get("/{company_id}")
def get_company(company_id: int):
    return companies[company_id]


