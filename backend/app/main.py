"""Main FastAPI + aiogram application"""

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from aiogram import Bot, Dispatcher
from app.config import settings
from app.database import init_db
from app.logger import get_logger
from app.bot.handlers import router as bot_router
from app.api.routes import nft, user, market

logger = get_logger()

# Initialize bot and dispatcher
bot = Bot(token=settings.bot_token)
dp = Dispatcher()

# Include handlers
dp.include_router(bot_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown"""
    # Startup
    logger.info("Application starting...")
    init_db()
    logger.info(f"Bot token: {settings.bot_token[:10]}...")
    logger.info(f"WebApp URL: {settings.webapp_url}")
    
    # Start polling
    asyncio.create_task(dp.start_polling(bot))
    logger.info("Bot polling started")
    
    yield
    
    # Shutdown
    logger.info("Application shutting down...")
    await bot.session.close()
    logger.info("Application stopped")


# Create FastAPI app
app = FastAPI(
    title="NFT Trading Bot API",
    description="API for NFT Gift Trading Bot",
    version="0.1.0",
    lifespan=lifespan
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(nft.router, prefix=settings.api_prefix)
app.include_router(user.router, prefix=settings.api_prefix)
app.include_router(market.router, prefix=settings.api_prefix)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "NFT Trading Bot API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "NFT Trading Bot"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
