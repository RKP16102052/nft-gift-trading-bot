"""NFT API routes"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import NFT, PriceHistory
from app.schemas import NFTResponse, NFTDetailResponse, NFTCreate, PriceHistoryResponse
from app.helpers import get_price_history_period, paginate
from app.logger import get_logger
from datetime import datetime

logger = get_logger()
router = APIRouter(prefix="/nft", tags=["nft"])


@router.get("/list", response_model=dict)
async def list_nfts(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    rarity: str = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of all NFTs"""
    try:
        query = db.query(NFT)
        
        if rarity:
            query = query.filter(NFT.rarity == rarity)
        
        nfts = query.all()
        paginated = paginate(nfts, page, per_page)
        
        return {
            "total": paginated["total"],
            "page": paginated["page"],
            "per_page": paginated["per_page"],
            "total_pages": paginated["total_pages"],
            "items": [NFTResponse.from_orm(nft).dict() for nft in paginated["items"]]
        }
    except Exception as e:
        logger.error(f"Error listing NFTs: {e}")
        raise HTTPException(status_code=500, detail="Error listing NFTs")


@router.get("/{nft_id}", response_model=NFTDetailResponse)
async def get_nft(nft_id: int, db: Session = Depends(get_db)):
    """Get NFT by ID"""
    try:
        nft = db.query(NFT).filter(NFT.id == nft_id).first()
        if not nft:
            raise HTTPException(status_code=404, detail="NFT not found")
        
        return NFTDetailResponse.from_orm(nft)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting NFT: {e}")
        raise HTTPException(status_code=500, detail="Error getting NFT")


@router.get("/{nft_id}/price-history", response_model=dict)
async def get_price_history(
    nft_id: int,
    days: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get NFT price history"""
    try:
        nft = db.query(NFT).filter(NFT.id == nft_id).first()
        if not nft:
            raise HTTPException(status_code=404, detail="NFT not found")
        
        start_date, end_date = get_price_history_period(days)
        
        history = db.query(PriceHistory).filter(
            PriceHistory.nft_id == nft_id,
            PriceHistory.timestamp >= start_date,
            PriceHistory.timestamp <= end_date
        ).order_by(PriceHistory.timestamp).all()
        
        return {
            "nft_id": nft_id,
            "nft_name": nft.name,
            "current_price": nft.current_price,
            "days": days,
            "history": [PriceHistoryResponse.from_orm(h).dict() for h in history]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting price history: {e}")
        raise HTTPException(status_code=500, detail="Error getting price history")


@router.post("/create", response_model=NFTResponse)
async def create_nft(nft_data: NFTCreate, db: Session = Depends(get_db)):
    """Create new NFT (admin only)"""
    try:
        # Check if NFT already exists
        existing = db.query(NFT).filter(NFT.name == nft_data.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="NFT with this name already exists")
        
        new_nft = NFT(**nft_data.dict())
        db.add(new_nft)
        db.commit()
        db.refresh(new_nft)
        
        logger.info(f"New NFT created: {new_nft.name}")
        
        return NFTResponse.from_orm(new_nft)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating NFT: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating NFT")
