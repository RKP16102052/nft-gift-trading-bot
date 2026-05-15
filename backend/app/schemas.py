"""Pydantic schemas for data validation"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


# User Schemas
class UserBase(BaseModel):
    telegram_id: str
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    balance: Optional[float] = None
    is_admin: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    balance: float
    created_at: datetime
    is_admin: bool

    class Config:
        from_attributes = True


# NFT Schemas
class NFTBase(BaseModel):
    name: str
    description: str
    image_url: str
    rarity: str = Field(..., pattern="^(common|uncommon|rare|epic|legendary)$")


class NFTCreate(NFTBase):
    current_price: float = 100.0


class NFTUpdate(BaseModel):
    current_price: Optional[float] = None
    description: Optional[str] = None


class NFTResponse(NFTBase):
    id: int
    current_price: float
    created_at: datetime

    class Config:
        from_attributes = True


class NFTDetailResponse(NFTResponse):
    user_nfts: Optional[List['UserNFTResponse']] = []
    listings: Optional[List['ListingResponse']] = []


# UserNFT Schemas
class UserNFTBase(BaseModel):
    user_id: int
    nft_id: int
    quantity: int = 1


class UserNFTCreate(UserNFTBase):
    acquired_price: float


class UserNFTResponse(UserNFTBase):
    id: int
    acquired_price: float
    acquired_at: datetime

    class Config:
        from_attributes = True


# Listing Schemas
class ListingBase(BaseModel):
    nft_id: int
    price: float
    quantity: int = 1


class ListingCreate(ListingBase):
    seller_id: int


class ListingUpdate(BaseModel):
    price: Optional[float] = None
    is_active: Optional[bool] = None


class ListingResponse(ListingBase):
    id: int
    seller_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Transaction Schemas
class TransactionBase(BaseModel):
    user_id: int
    nft_id: int
    transaction_type: str
    amount: float
    quantity: int = 1
    price_per_unit: float


class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Price History Schemas
class PriceHistoryBase(BaseModel):
    nft_id: int
    price: float


class PriceHistoryResponse(PriceHistoryBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


# Market Schemas
class BuyNFTRequest(BaseModel):
    listing_id: int
    quantity: int = 1


class SellNFTRequest(BaseModel):
    nft_id: int
    price: float
    quantity: int = 1


class CancelListingRequest(BaseModel):
    listing_id: int
