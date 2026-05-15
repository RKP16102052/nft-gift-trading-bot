"""SQLAlchemy models for NFT Trading Bot"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True, index=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    balance = Column(Float, default=1000.0)  # Стартовый баланс
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_admin = Column(Boolean, default=False)
    
    # Relationships
    nfts = relationship("UserNFT", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    listings = relationship("Listing", back_populates="seller")


class NFT(Base):
    """NFT model"""
    __tablename__ = "nfts"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    image_url = Column(String)
    rarity = Column(String)  # common, uncommon, rare, epic, legendary
    created_at = Column(DateTime, default=datetime.utcnow)
    current_price = Column(Float, default=100.0)
    
    # Relationships
    user_nfts = relationship("UserNFT", back_populates="nft")
    listings = relationship("Listing", back_populates="nft")
    price_history = relationship("PriceHistory", back_populates="nft")


class UserNFT(Base):
    """User's NFT ownership model"""
    __tablename__ = "user_nfts"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    nft_id = Column(Integer, ForeignKey("nfts.id"))
    quantity = Column(Integer, default=1)
    acquired_price = Column(Float)  # По какой цене был куплен
    acquired_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="nfts")
    nft = relationship("NFT", back_populates="user_nfts")


class Listing(Base):
    """NFT listing on marketplace"""
    __tablename__ = "listings"
    
    id = Column(Integer, primary_key=True)
    nft_id = Column(Integer, ForeignKey("nfts.id"))
    seller_id = Column(Integer, ForeignKey("users.id"))
    price = Column(Float)
    quantity = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    nft = relationship("NFT", back_populates="listings")
    seller = relationship("User", back_populates="listings")


class TransactionType(str, enum.Enum):
    """Transaction types"""
    BUY = "buy"
    SELL = "sell"
    TRANSFER = "transfer"
    REWARD = "reward"


class Transaction(Base):
    """Transaction history"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    nft_id = Column(Integer, ForeignKey("nfts.id"))
    transaction_type = Column(Enum(TransactionType))
    amount = Column(Float)  # Количество денег
    quantity = Column(Integer, default=1)  # Количество NFT
    price_per_unit = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="transactions")


class PriceHistory(Base):
    """NFT price history for charts"""
    __tablename__ = "price_history"
    
    id = Column(Integer, primary_key=True)
    nft_id = Column(Integer, ForeignKey("nfts.id"))
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    nft = relationship("NFT", back_populates="price_history")
