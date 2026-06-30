from fastapi import FastAPI
from routers import job
from routers import company
from models import job as job_model, company as company_model
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(company.router)
app.include_router(job.router)
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/about")
def read_about():
    return {"About": "This is a FastAPI application."}

@app.get("/contact")
def read_contact():
    return {"Contact": "dhruvkum93@gmail.com"} 