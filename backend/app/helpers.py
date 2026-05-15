"""Helper functions and utilities"""

import hashlib
import hmac
import json
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import math


def verify_telegram_webapp(init_data: str, bot_token: str) -> bool:
    """
    Verify Telegram WebApp data
    
    Args:
        init_data: Web App init data
        bot_token: Bot token
    
    Returns:
        bool: True if valid
    """
    try:
        params = dict(x.split('=') for x in init_data.split('&'))
        if 'hash' not in params:
            return False
        
        hash_value = params.pop('hash')
        
        # Create data check string
        data_check_string = '\n'.join(
            f'{k}={v}' for k, v in sorted(params.items())
        )
        
        # Create secret key
        secret_key = hmac.new(
            b'WebAppData',
            bot_token.encode(),
            hashlib.sha256
        ).digest()
        
        # Create hash
        computed_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return computed_hash == hash_value
    except Exception as e:
        print(f"WebApp verification error: {e}")
        return False


def format_price(price: float) -> str:
    """
    Format price for display
    
    Args:
        price: Price value
    
    Returns:
        str: Formatted price
    """
    if price >= 1_000_000:
        return f"{price / 1_000_000:.1f}M"
    elif price >= 1_000:
        return f"{price / 1_000:.1f}K"
    else:
        return f"{price:.2f}"


def format_currency(amount: float, currency: str = "💎") -> str:
    """
    Format currency for display
    
    Args:
        amount: Amount
        currency: Currency symbol
    
    Returns:
        str: Formatted currency
    """
    return f"{currency} {amount:,.2f}"


def calculate_price_change(old_price: float, new_price: float) -> Dict[str, Any]:
    """
    Calculate price change percentage and direction
    
    Args:
        old_price: Old price
        new_price: New price
    
    Returns:
        dict: Change info
    """
    if old_price == 0:
        return {"percentage": 0, "direction": "➡️", "change": 0}
    
    change_percent = ((new_price - old_price) / old_price) * 100
    direction = "📈" if change_percent > 0 else "📉" if change_percent < 0 else "➡️"
    
    return {
        "percentage": abs(change_percent),
        "direction": direction,
        "change": new_price - old_price
    }


def get_price_history_period(days: int) -> tuple:
    """
    Get time period for price history
    
    Args:
        days: Number of days
    
    Returns:
        tuple: (start_date, end_date)
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def paginate(items: list, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    """
    Paginate a list
    
    Args:
        items: List of items
        page: Page number
        per_page: Items per page
    
    Returns:
        dict: Paginated data
    """
    total = len(items)
    total_pages = math.ceil(total / per_page)
    
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "items": items[start:end]
    }


def generate_nft_emoji(rarity: str) -> str:
    """
    Generate emoji based on rarity
    
    Args:
        rarity: NFT rarity
    
    Returns:
        str: Emoji
    """
    emojis = {
        "common": "🟢",
        "uncommon": "🔵",
        "rare": "🟣",
        "epic": "🟠",
        "legendary": "🟡"
    }
    return emojis.get(rarity, "🎁")
