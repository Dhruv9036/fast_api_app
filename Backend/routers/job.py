from fastapi import APIRouter, HTTPException, Depends, status
from models import company, job
from sqlalchemy.orm import Session
from database import get_db
from schemas.job import JobCreate, JobUpdate, JobResponse   

router = APIRouter(prefix="/job", tags=["job"])
jobs=[]




@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=JobResponse
)
def create_job(job_data: JobCreate, db: Session = Depends(get_db)):
    db_job = job.Job(
        title=job_data.title,
        description=job_data.description,
        company_id=job_data.company_id,
        salary=job_data.salary
    )

    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    return db_job

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[JobResponse])
def get_all_jobs(db: Session = Depends(get_db)):
    return db.query(job.Job).all()

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(job.Job).filter(job.Job.id == job_id).first()

    if db_job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    return db_job


@router.put("/{job_id}", response_model=JobResponse)
def update_job(job_id: int, job_data: JobUpdate, db: Session = Depends(get_db)):    
    db_job = db.query(job.Job).filter(job.Job.id == job_id).first()

    if db_job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    for key, value in job_data.dict(exclude_unset=True).items():
        setattr(db_job, key, value)

    db.commit()
    db.refresh(db_job)

    return db_job       

@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(job.Job).filter(job.Job.id == job_id).first()

    if db_job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    db.delete(db_job)
    db.commit()

    return {"message": "Job deleted successfully."}


# @router.get("/")
# def read_job():
#     return {"Job": "Job Root"}

# @router.get("/{job_id}")
# def read_job_id(job_id: int):
#     return {"Job ID": job_id}
