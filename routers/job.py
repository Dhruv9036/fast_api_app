from fastapi import APIRouter
from schemas.company import CompanyCreate
from schemas.job import JobCreate, JobUpdate   

router = APIRouter(prefix="/job", tags=["job"])
jobs=[]




@router.post("/")
def create_job(jobs: JobCreate):
    jobs.append(jobs)
    return jobs      

@router.get("/")
def get_all_job():
    return jobs

@router.get("/{job_id}")
def get_job(job_id: int):
    return jobs[job_id]


@router.put("/{job_id}")
def update_job(job_id: int, job: JobUpdate):
    jobs[job_id] = job
    return jobs

@router.delete("/{job_id}")
def delete_job(job_id: int):        
    del jobs[job_id]
    return {"message": "Job deleted successfully."}


# @router.get("/")
# def read_job():
#     return {"Job": "Job Root"}

# @router.get("/{job_id}")
# def read_job_id(job_id: int):
#     return {"Job ID": job_id}
