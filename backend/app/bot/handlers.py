"""Telegram bot handlers"""

from aiogram import Router, F, types
from aiogram.filters import Command, CommandStart
from aiogram.types import WebAppInfo
from app.config import settings
from app.logger import get_logger
from app.database import SessionLocal
from app.models import User

logger = get_logger()
router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    """Handle /start command"""
    user_id = str(message.from_user.id)
    
    # Get or create user
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.telegram_id == user_id).first()
        if not user:
            user = User(
                telegram_id=user_id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                balance=1000.0
            )
            db.add(user)
            db.commit()
            logger.info(f"New user created: {user_id}")
        else:
            logger.info(f"User logged in: {user_id}")
    except Exception as e:
        logger.error(f"Error in start handler: {e}")
        db.rollback()
    finally:
        db.close()
    
    # Send welcome message with WebApp button
    await message.answer(
        "🎁 Добро пожаловать в NFT Gift Trading Bot!\n\n"
        "💰 Торгуйте NFT-подарками, отслеживайте цены и зарабатывайте!\n\n"
        "Нажмите кнопку ниже, чтобы открыть приложение:",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="🚀 Открыть маркетплейс",
                        web_app=WebAppInfo(url=settings.webapp_url)
                    )
                ]
            ]
        )
    )


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """Handle /help command"""
    await message.answer(
        "📖 Справка по командам:\n\n"
        "/start - Начало работы\n"
        "/portfolio - Мой портфель NFT\n"
        "/help - Эта справка\n"
        "/admin - Админ-панель (только для админов)",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="🚀 Открыть приложение",
                        web_app=WebAppInfo(url=settings.webapp_url)
                    )
                ]
            ]
        )
    )


@router.message(Command("portfolio"))
async def cmd_portfolio(message: types.Message):
    """Handle /portfolio command"""
    user_id = str(message.from_user.id)
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.telegram_id == user_id).first()
        if user:
            nft_count = len(user.nfts)
            await message.answer(
                f"💼 Ваш портфель:\n\n"
                f"👤 Пользователь: {user.first_name}\n"
                f"💎 Баланс: {user.balance:.2f}\n"
                f"🎁 NFT в портфеле: {nft_count}\n\n"
                f"Откройте приложение для подробной информации:",
                reply_markup=types.InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            types.InlineKeyboardButton(
                                text="💼 Мой портфель",
                                web_app=WebAppInfo(url=f"{settings.webapp_url}/portfolio")
                            )
                        ]
                    ]
                )
            )
        else:
            await message.answer("❌ Пользователь не найден")
    except Exception as e:
        logger.error(f"Error in portfolio handler: {e}")
        await message.answer("❌ Ошибка при получении портфеля")
    finally:
        db.close()


@router.message(Command("admin"))
async def cmd_admin(message: types.Message):
    """Handle /admin command"""
    user_id = str(message.from_user.id)
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.telegram_id == user_id).first()
        if user and user.is_admin:
            await message.answer(
                "🔧 Админ-панель:\n\n"
                "/logs - Скачать логи\n"
                "/stats - Статистика\n"
                "/users - Список пользователей\n\n"
                "Откройте полную админ-панель:",
                reply_markup=types.InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            types.InlineKeyboardButton(
                                text="🔧 Админ-панель",
                                web_app=WebAppInfo(url=f"{settings.webapp_url}/admin")
                            )
                        ]
                    ]
                )
            )
        else:
            await message.answer("❌ У вас нет доступа к админ-панели")
    except Exception as e:
        logger.error(f"Error in admin handler: {e}")
        await message.answer("❌ Ошибка при доступе к админ-панели")
    finally:
        db.close()


@router.message()
async def echo_handler(message: types.Message):
    """Echo handler for unknown messages"""
    await message.answer(
        "Я не понял вашу команду.\n"
        "Используйте /help для справки или нажмите кнопку ниже:",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="🚀 Открыть приложение",
                        web_app=WebAppInfo(url=settings.webapp_url)
                    )
                ]
            ]
        )
    )
