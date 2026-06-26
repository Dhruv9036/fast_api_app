from fastapi import APIRouter
router = APIRouter(prefix="/job",tags={"job"})


@router.get("/")
def read_company():
    return{"company":"company root"}