from fastapi import APIRouter


router = APIRouter(prefix="/users")

@router.get("/")
def get_all_users():
    pass

@router.get("/me")
def get_user():
    pass