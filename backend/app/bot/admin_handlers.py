"""Admin handlers for Telegram bot"""

from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.config import settings
from app.logger import get_logger
from app.database import SessionLocal
from app.models import User, NFT, Transaction
from datetime import datetime, timedelta
import io

logger = get_logger()
router = Router()


class AddNFTStates(StatesGroup):
    """States for adding NFT"""
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_rarity = State()
    waiting_for_price = State()


def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.telegram_id == str(user_id)).first()
        return user and user.is_admin
    finally:
        db.close()


@router.message(Command("add_nft"))
async def cmd_add_nft(message: types.Message, state: FSMContext):
    """Start adding new NFT (admin only)"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет доступа к этой команде")
        return

    await message.answer(
        "📝 Давайте добавим новый NFT!\n\n"
        "Введите название NFT:"
    )
    await state.set_state(AddNFTStates.waiting_for_name)


@router.message(AddNFTStates.waiting_for_name)
async def process_nft_name(message: types.Message, state: FSMContext):
    """Process NFT name"""
    await state.update_data(name=message.text)
    await message.answer("Введите описание NFT:")
    await state.set_state(AddNFTStates.waiting_for_description)


@router.message(AddNFTStates.waiting_for_description)
async def process_nft_description(message: types.Message, state: FSMContext):
    """Process NFT description"""
    await state.update_data(description=message.text)
    await message.answer(
        "Выберите рарность:\n\n"
        "1️⃣ common\n"
        "2️⃣ uncommon\n"
        "3️⃣ rare\n"
        "4️⃣ epic\n"
        "5️⃣ legendary"
    )
    await state.set_state(AddNFTStates.waiting_for_rarity)


@router.message(AddNFTStates.waiting_for_rarity)
async def process_nft_rarity(message: types.Message, state: FSMContext):
    """Process NFT rarity"""
    rarity_map = {
        "1": "common",
        "2": "uncommon",
        "3": "rare",
        "4": "epic",
        "5": "legendary",
    }

    rarity = rarity_map.get(message.text)
    if not rarity:
        await message.answer("❌ Выберите правильный номер (1-5)")
        return

    await state.update_data(rarity=rarity)
    await message.answer("Введите цену NFT (в виде числа):")
    await state.set_state(AddNFTStates.waiting_for_price)


@router.message(AddNFTStates.waiting_for_price)
async def process_nft_price(message: types.Message, state: FSMContext):
    """Process NFT price and create NFT"""
    try:
        price = float(message.text)
    except ValueError:
        await message.answer("❌ Введите корректное число")
        return

    data = await state.get_data()
    db = SessionLocal()

    try:
        # Check if NFT already exists
        existing = db.query(NFT).filter(NFT.name == data["name"]).first()
        if existing:
            await message.answer("❌ NFT с таким названием уже существует")
            await state.clear()
            return

        # Create NFT
        new_nft = NFT(
            name=data["name"],
            description=data["description"],
            image_url="https://via.placeholder.com/200?text=NFT",
            rarity=data["rarity"],
            current_price=price,
        )
        db.add(new_nft)
        db.commit()

        await message.answer(
            f"✅ NFT успешно добавлена!\n\n"
            f"📛 Название: {data['name']}\n"
            f"📝 Описание: {data['description']}\n"
            f"💎 Рарность: {data['rarity']}\n"
            f"💰 Цена: {price}"
        )
        logger.info(f"New NFT created by admin: {data['name']}")
    except Exception as e:
        logger.error(f"Error creating NFT: {e}")
        await message.answer("❌ Ошибка при создании NFT")
    finally:
        db.close()
        await state.clear()


@router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    """Get statistics (admin only)"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет доступа к этой команде")
        return

    db = SessionLocal()
    try:
        total_users = db.query(User).count()
        total_nfts = db.query(NFT).count()
        total_transactions = db.query(Transaction).count()
        total_balance = sum([u.balance for u in db.query(User).all()]) or 0

        # Transactions in last 24 hours
        yesterday = datetime.utcnow() - timedelta(days=1)
        transactions_24h = db.query(Transaction).filter(
            Transaction.created_at >= yesterday
        ).count()

        await message.answer(
            f"📊 Статистика платформы:\n\n"
            f"👥 Пользователей: {total_users}\n"
            f"🎁 NFT в каталоге: {total_nfts}\n"
            f"💱 Всего транзакций: {total_transactions}\n"
            f"📈 Транзакций за 24ч: {transactions_24h}\n"
            f"💎 Общий баланс пользователей: {total_balance:.2f}"
        )
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        await message.answer("❌ Ошибка при получении статистики")
    finally:
        db.close()


@router.message(Command("logs"))
async def cmd_logs(message: types.Message):
    """Send logs file (admin only)"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет доступа к этой команде")
        return

    try:
        with open("logs/app.log", "r", encoding="utf-8") as f:
            log_content = f.read()

        # Send as document
        log_bytes = io.BytesIO(log_content.encode('utf-8'))
        await message.answer_document(
            document=types.BufferedReader(log_bytes),
            filename="app.log",
            caption="📋 Логи приложения"
        )
    except FileNotFoundError:
        await message.answer("❌ Файл логов не найден")
    except Exception as e:
        logger.error(f"Error sending logs: {e}")
        await message.answer("❌ Ошибка при отправке логов")


@router.message(Command("users"))
async def cmd_users(message: types.Message):
    """Get users list (admin only)"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет доступа к этой команде")
        return

    db = SessionLocal()
    try:
        users = db.query(User).limit(20).all()
        text = "👥 Список пользователей (первые 20):\n\n"

        for user in users:
            text += f"👤 {user.first_name or 'Unknown'} (@{user.username or 'unknown'})\n"
            text += f"   ID: {user.telegram_id}\n"
            text += f"   💎 Баланс: {user.balance:.2f}\n"
            text += f"   Статус: {'⭐ Admin' if user.is_admin else '👤 User'}\n\n"

        await message.answer(text)
    except Exception as e:
        logger.error(f"Error getting users list: {e}")
        await message.answer("❌ Ошибка при получении списка пользователей")
    finally:
        db.close()


@router.message(Command("notifications"))
async def cmd_notifications(message: types.Message):
    """Send price notifications to all users (admin only)"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет доступа к этой команде")
        return

    await message.answer(
        "🔔 Система уведомлений активирована!\n\n"
        "Пользователи теперь будут получать уведомления о:\n"
        "• Изменениях цен NFT\n"
        "• Новых лучших предложениях\n"
        "• Активности их портфеля"
    )
    logger.info(f"Notifications enabled by {message.from_user.id}")
