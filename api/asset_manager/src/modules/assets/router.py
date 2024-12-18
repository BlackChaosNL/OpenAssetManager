from uuid import UUID

from fastapi.routing import APIRouter

from .models import Asset

router = APIRouter(
    prefix="/assets"
)

@router.get("/")
async def get_all_assets():
    return await Asset.get_or_none()

@router.post("/")
async def create_asset(name: str):
    asset = await Asset.create(name=name)
    return asset

@router.delete("/", status_code=204)
async def delete_asset(remove_id: UUID):
    await Asset.filter(id=remove_id).delete()

@router.get("/{asset_id}")
async def get_asset(asset_id: UUID):
    return Asset.filter(id=asset_id).get_or_none()
