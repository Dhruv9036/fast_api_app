from sqlalchemy import Column, Integer, String, Enum, ForeignKey 
from sqlalchemy.orm import relationship
from models.company import Company
from database import Base, engine, SessionLocal

class Job(Base):
    __tablename__ = 'jobs'

    company = relationship("Company", back_populates="jobs")
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    salary = Column(Integer, nullable=False)