from fastapi import APIRouter


router = APIRouter(prefix="/organizations")

@router.get("/")
def all_organizations():
    pass

@router.delete("/")
def delete_organization():
    pass

@router.post("/create")
def create_organization():
    pass

