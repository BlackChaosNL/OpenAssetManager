from fastapi import APIRouter


router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("/")
def get_all_users():
    pass


@router.post("/")
def create_user():
    pass


@router.get("/me")
def get_user():
    pass
