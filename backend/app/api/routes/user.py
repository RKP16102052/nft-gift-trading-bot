"""User API routes"""

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, UserNFT
from app.schemas import UserResponse, UserCreate, UserUpdate
from app.helpers import verify_telegram_webapp
from app.config import settings
from app.logger import get_logger
import json
from urllib.parse import unquote

logger = get_logger()
router = APIRouter(prefix="/user", tags=["user"])


def verify_user(x_init_data: str = Header(None), db: Session = Depends(get_db)) -> User:
    """Verify and get current user from WebApp data"""
    if not x_init_data:
        raise HTTPException(status_code=401, detail="Missing authentication")
    
    # Verify WebApp data
    if not verify_telegram_webapp(x_init_data, settings.bot_token):
        raise HTTPException(status_code=401, detail="Invalid authentication")
    
    # Parse user data
    try:
        params = dict(x.split('=') for x in x_init_data.split('&'))
        user_data = json.loads(unquote(params.get('user', '{}')))
        telegram_id = str(user_data.get('id'))
    except Exception as e:
        logger.error(f"Error parsing user data: {e}")
        raise HTTPException(status_code=401, detail="Invalid user data")
    
    # Get or create user
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        user = User(
            telegram_id=telegram_id,
            username=user_data.get('username'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            balance=1000.0
        )
        db.add(user)
        db.commit()
        logger.info(f"New user created via API: {telegram_id}")
    
    return user


@router.get("/me", response_model=UserResponse)
async def get_current_user(user: User = Depends(verify_user)):
    """Get current user info"""
    return UserResponse.from_orm(user)


@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Register new user"""
    try:
        # Check if user already exists
        existing = db.query(User).filter(User.telegram_id == user_data.telegram_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")
        
        new_user = User(**user_data.dict(), balance=1000.0)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        logger.info(f"New user registered: {user_data.telegram_id}")
        
        return UserResponse.from_orm(new_user)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error registering user")


@router.get("/portfolio", response_model=dict)
async def get_portfolio(user: User = Depends(verify_user), db: Session = Depends(get_db)):
    """Get user portfolio"""
    try:
        user_nfts = db.query(UserNFT).filter(UserNFT.user_id == user.id).all()
        
        total_value = sum(nft.nft.current_price * nft.quantity for nft in user_nfts)
        
        return {
            "user_id": user.id,
            "balance": user.balance,
            "total_nfts": len(user_nfts),
            "portfolio_value": total_value,
            "total_value": user.balance + total_value,
            "nfts": [
                {
                    "nft_id": nft.nft_id,
                    "name": nft.nft.name,
                    "quantity": nft.quantity,
                    "acquired_price": nft.acquired_price,
                    "current_price": nft.nft.current_price,
                    "value": nft.nft.current_price * nft.quantity,
                    "profit": (nft.nft.current_price - nft.acquired_price) * nft.quantity
                }
                for nft in user_nfts
            ]
        }
    except Exception as e:
        logger.error(f"Error getting portfolio: {e}")
        raise HTTPException(status_code=500, detail="Error getting portfolio")


@router.post("/add-balance", response_model=UserResponse)
async def add_balance(
    amount: float,
    user: User = Depends(verify_user),
    db: Session = Depends(get_db)
):
    """Add balance to user (admin only)"""
    try:
        if amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be positive")
        
        user.balance += amount
        db.commit()
        db.refresh(user)
        
        logger.info(f"Balance added to user {user.telegram_id}: +{amount}")
        
        return UserResponse.from_orm(user)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding balance: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error adding balance")
