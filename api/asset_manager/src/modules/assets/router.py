from uuid import UUID

from fastapi.routing import APIRouter

router = APIRouter(
    prefix="/assets"
)

@router.get("/")
async def get_all_assets():
    pass

@router.post("/")
async def create_asset(name: str):
    pass

@router.delete("/", status_code=204)
async def delete_asset(remove_id: UUID):
    pass

@router.get("/{asset_id}")
async def get_asset(asset_id: UUID):
    pass
