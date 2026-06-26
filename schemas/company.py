from pydantic import BaseModel
from company import optional

class CompanyCreate(BaseModel):
    name: str
    location: str

class CompanyUpdate(BaseModel):
    name: Optional[str]   = None
    location: Optional[str] = None