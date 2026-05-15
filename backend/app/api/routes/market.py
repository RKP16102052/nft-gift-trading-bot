"""Market API routes"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, NFT, Listing, Transaction, TransactionType, UserNFT, PriceHistory
from app.schemas import ListingResponse, ListingCreate, TransactionResponse, SellNFTRequest, BuyNFTRequest
from app.api.routes.user import verify_user
from app.helpers import paginate
from app.logger import get_logger
from datetime import datetime

logger = get_logger()
router = APIRouter(prefix="/market", tags=["market"])


@router.get("/listings", response_model=dict)
async def get_listings(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get active market listings"""
    try:
        query = db.query(Listing).filter(Listing.is_active == True)
        listings = query.all()
        paginated = paginate(listings, page, per_page)
        
        return {
            "total": paginated["total"],
            "page": paginated["page"],
            "per_page": paginated["per_page"],
            "total_pages": paginated["total_pages"],
            "items": [
                {
                    "id": listing.id,
                    "nft_id": listing.nft_id,
                    "nft_name": listing.nft.name,
                    "nft_rarity": listing.nft.rarity,
                    "seller_id": listing.seller_id,
                    "price": listing.price,
                    "quantity": listing.quantity,
                    "created_at": listing.created_at
                }
                for listing in paginated["items"]
            ]
        }
    except Exception as e:
        logger.error(f"Error getting listings: {e}")
        raise HTTPException(status_code=500, detail="Error getting listings")


@router.post("/sell", response_model=ListingResponse)
async def sell_nft(
    request: SellNFTRequest,
    user: User = Depends(verify_user),
    db: Session = Depends(get_db)
):
    """List NFT for sale"""
    try:
        # Check if user owns the NFT
        user_nft = db.query(UserNFT).filter(
            UserNFT.user_id == user.id,
            UserNFT.nft_id == request.nft_id,
            UserNFT.quantity >= request.quantity
        ).first()
        
        if not user_nft:
            raise HTTPException(status_code=400, detail="Insufficient NFT quantity")
        
        # Get NFT
        nft = db.query(NFT).filter(NFT.id == request.nft_id).first()
        if not nft:
            raise HTTPException(status_code=404, detail="NFT not found")
        
        # Create listing
        listing = Listing(
            nft_id=request.nft_id,
            seller_id=user.id,
            price=request.price,
            quantity=request.quantity,
            is_active=True
        )
        
        db.add(listing)
        db.commit()
        db.refresh(listing)
        
        logger.info(f"Listing created: {listing.id} by user {user.telegram_id}")
        
        return ListingResponse.from_orm(listing)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating listing: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating listing")


@router.post("/cancel", response_model=dict)
async def cancel_listing(
    listing_id: int,
    user: User = Depends(verify_user),
    db: Session = Depends(get_db)
):
    """Cancel active listing"""
    try:
        listing = db.query(Listing).filter(
            Listing.id == listing_id,
            Listing.seller_id == user.id,
            Listing.is_active == True
        ).first()
        
        if not listing:
            raise HTTPException(status_code=404, detail="Listing not found")
        
        listing.is_active = False
        db.commit()
        
        logger.info(f"Listing canceled: {listing_id}")
        
        return {"message": "Listing canceled successfully", "listing_id": listing_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error canceling listing: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error canceling listing")


@router.post("/buy", response_model=TransactionResponse)
async def buy_nft(
    request: BuyNFTRequest,
    user: User = Depends(verify_user),
    db: Session = Depends(get_db)
):
    """Buy NFT from listing"""
    try:
        # Get listing
        listing = db.query(Listing).filter(
            Listing.id == request.listing_id,
            Listing.is_active == True
        ).first()
        
        if not listing:
            raise HTTPException(status_code=404, detail="Listing not found")
        
        if listing.quantity < request.quantity:
            raise HTTPException(status_code=400, detail="Insufficient quantity")
        
        # Calculate total price
        total_price = listing.price * request.quantity
        
        # Check user balance
        if user.balance < total_price:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        
        # Get NFT
        nft = db.query(NFT).filter(NFT.id == listing.nft_id).first()
        
        # Create transaction
        transaction = Transaction(
            user_id=user.id,
            nft_id=listing.nft_id,
            transaction_type=TransactionType.BUY,
            amount=total_price,
            quantity=request.quantity,
            price_per_unit=listing.price
        )
        
        # Update balances
        user.balance -= total_price
        seller = db.query(User).filter(User.id == listing.seller_id).first()
        seller.balance += total_price
        
        # Update or create user NFT
        user_nft = db.query(UserNFT).filter(
            UserNFT.user_id == user.id,
            UserNFT.nft_id == listing.nft_id
        ).first()
        
        if user_nft:
            user_nft.quantity += request.quantity
        else:
            user_nft = UserNFT(
                user_id=user.id,
                nft_id=listing.nft_id,
                quantity=request.quantity,
                acquired_price=listing.price
            )
            db.add(user_nft)
        
        # Decrease seller's NFT quantity
        seller_nft = db.query(UserNFT).filter(
            UserNFT.user_id == listing.seller_id,
            UserNFT.nft_id == listing.nft_id
        ).first()
        
        if seller_nft:
            seller_nft.quantity -= request.quantity
        
        # Update listing
        listing.quantity -= request.quantity
        if listing.quantity == 0:
            listing.is_active = False
        
        # Add price history entry
        price_history = PriceHistory(
            nft_id=listing.nft_id,
            price=listing.price
        )
        db.add(price_history)
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        logger.info(f"NFT purchased: {listing.nft_id} by user {user.telegram_id}")
        
        return TransactionResponse.from_orm(transaction)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error buying NFT: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error buying NFT")


@router.get("/orders", response_model=dict)
async def get_user_orders(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    user: User = Depends(verify_user),
    db: Session = Depends(get_db)
):
    """Get user transaction history"""
    try:
        transactions = db.query(Transaction).filter(
            Transaction.user_id == user.id
        ).order_by(Transaction.created_at.desc()).all()
        
        paginated = paginate(transactions, page, per_page)
        
        return {
            "total": paginated["total"],
            "page": paginated["page"],
            "per_page": paginated["per_page"],
            "total_pages": paginated["total_pages"],
            "items": [TransactionResponse.from_orm(t).dict() for t in paginated["items"]]
        }
    except Exception as e:
        logger.error(f"Error getting orders: {e}")
        raise HTTPException(status_code=500, detail="Error getting orders")
