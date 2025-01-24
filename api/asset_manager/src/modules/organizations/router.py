from fastapi import APIRouter


router = APIRouter(prefix="/api/v1/organizations")

@router.get("/")
def all_organizations():
    pass

@router.delete("/")
def delete_organization():
    pass

@router.post("/create")
def create_organization():
    pass

