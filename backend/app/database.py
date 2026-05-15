"""Database initialization and configuration"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings
from app.models import Base, NFT, User
from app.logger import get_logger
import os

logger = get_logger()

# Create engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
    echo=settings.debug
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database and create tables"""
    logger.info("Initializing database...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
    
    # Add initial NFTs if they don't exist
    db = SessionLocal()
    try:
        existing_nfts = db.query(NFT).count()
        if existing_nfts == 0:
            logger.info("Adding initial NFTs...")
            initial_nfts = [
                NFT(
                    name="Rare Dragon",
                    description="Легендарный дракон с магическими способностями",
                    image_url="https://via.placeholder.com/200?text=Dragon",
                    rarity="legendary",
                    current_price=5000.0
                ),
                NFT(
                    name="Golden Phoenix",
                    description="Золотой феникс, символ возрождения",
                    image_url="https://via.placeholder.com/200?text=Phoenix",
                    rarity="epic",
                    current_price=3000.0
                ),
                NFT(
                    name="Silver Unicorn",
                    description="Серебристый единорог с волшебными рогами",
                    image_url="https://via.placeholder.com/200?text=Unicorn",
                    rarity="epic",
                    current_price=2500.0
                ),
                NFT(
                    name="Mystical Wolf",
                    description="Мистический волк из древних лесов",
                    image_url="https://via.placeholder.com/200?text=Wolf",
                    rarity="rare",
                    current_price=1500.0
                ),
                NFT(
                    name="Ice Queen",
                    description="Ледяная королева с кристальной короной",
                    image_url="https://via.placeholder.com/200?text=Queen",
                    rarity="rare",
                    current_price=1200.0
                ),
                NFT(
                    name="Forest Guardian",
                    description="Хранитель леса, защитник природы",
                    image_url="https://via.placeholder.com/200?text=Guardian",
                    rarity="uncommon",
                    current_price=500.0
                ),
                NFT(
                    name="Sky Rider",
                    description="Всадник неба, покоритель облаков",
                    image_url="https://via.placeholder.com/200?text=Rider",
                    rarity="uncommon",
                    current_price=400.0
                ),
                NFT(
                    name="Cute Bunny",
                    description="Милый кролик с длинными ушами",
                    image_url="https://via.placeholder.com/200?text=Bunny",
                    rarity="common",
                    current_price=100.0
                ),
            ]
            db.add_all(initial_nfts)
            db.commit()
            logger.info(f"Added {len(initial_nfts)} initial NFTs")
    except Exception as e:
        logger.error(f"Error adding initial NFTs: {e}")
        db.rollback()
    finally:
        db.close()


def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
