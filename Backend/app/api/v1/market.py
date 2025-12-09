from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import PriceIn, PriceOut, AssetOut
from app.crud import assets as assets_crud, prices as prices_crud
from app.api.deps import get_db_session, get_current_user

router = APIRouter(prefix="/market", tags=["market"])


@router.post("/prices/ingest")
async def ingest_price(
    payload: PriceIn,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    asset = await assets_crud.create_asset_if_not_exists(db, payload.asset_symbol)
    price = await prices_crud.create_price(
        db,
        asset_id=asset.id,
        timestamp=payload.timestamp,
        open=payload.open,
        high=payload.high,
        low=payload.low,
        close=payload.close,
        volume=payload.volume,
    )
    return {"status": "ok", "price_id": price.id}


@router.get("/assets/{symbol}", response_model=AssetOut)
async def get_asset(
    symbol: str,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    asset = await assets_crud.get_asset_by_symbol(db, symbol)
    if not asset:
        raise HTTPException(404, "Asset not found")
    return asset


@router.get("/prices/{symbol}", response_model=list[PriceOut])
async def get_recent_prices(
    symbol: str,
    limit: int = 100,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    asset = await assets_crud.get_asset_by_symbol(db, symbol)
    if not asset:
        raise HTTPException(404, "Asset not found")
    prices = await prices_crud.get_recent_prices(db, asset.id, limit)
    return prices[::-1]  # return oldest → newest
