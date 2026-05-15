# NFT Gift Trading Bot 🎁

Телеграм бот для торговли NFT-подарками с WebApp, маркетплейсом и графиками цен в реальном времени.

## 🎯 Функционал

### Пользовательская часть
- ✅ WebApp интеграция (открытие прямо из бота)
- ✅ Маркетплейс NFT-подарков
- ✅ Выставление своих NFT на продажу
- ✅ Покупка чужих NFT (виртуальная валюта)
- ✅ История транзакций
- ✅ Личный портфель
- ✅ **Интерактивные графики цен** (история за дни/недели)
- ✅ Отслеживание динамики как на бирже

### Админ-часть
- ✅ Команда `/admin` - админ-панель
- ✅ Добавление новых NFT
- ✅ Выгрузка логов
- ✅ Просмотр статистики
- ✅ Управление пользователями

## 🛠 Технологический стек

### Backend
- **Python 3.13.1** - язык
- **aiogram 3.x** - Telegram бот
- **FastAPI** - REST API для WebApp
- **SQLite** - база данных
- **SQLAlchemy** - ORM
- **Pydantic** - валидация данных
- **uvicorn** - ASGI сервер

### Frontend
- **React 18** - UI фреймворк
- **TypeScript** - типизация
- **Tailwind CSS** - стили (розовая тема)
- **Chart.js / React-Chartjs-2** - графики цен
- **Axios** - HTTP клиент
- **Zustand** - state management

### DevOps
- **Docker** - контейнеризация
- **Railway** - хостинг
- **GitHub** - версионный контроль

## 📁 Структура проекта

```
nft-gift-trading-bot/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI + aiogram приложение
│   │   ├── config.py          # Конфигурация
│   │   ├── database.py        # SQLAlchemy, инициализация БД
│   │   ├── models.py          # SQLAlchemy модели
│   │   ├── schemas.py         # Pydantic схемы
│   │   ├── logger.py          # Логирование
│   │   ├── helpers.py         # Утилиты
│   │   ├── bot/
│   │   │   ├── __init__.py
│   │   │   └── handlers.py    # Handlers бота
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes/
│   │   │       ├── __init__.py
│   │   │       ├── nft.py      # NFT endpoints
│   │   │       ├── user.py     # User endpoints
│   │   │       ├── market.py   # Market endpoints
│   │   │       └── prices.py   # Price history endpoints
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── user_service.py
│   │       ├── nft_service.py
│   │       ├── market_service.py
│   │       └── price_service.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.tsx
│   │   │   ├── NFTCard.tsx
│   │   │   ├── PriceChart.tsx
│   │   │   ├── MarketplaceList.tsx
│   │   │   ├── PortfolioPage.tsx
│   │   │   └── AdminPanel.tsx
│   │   ├── pages/
│   │   │   ├── HomePage.tsx
│   │   │   ├── MarketplacePage.tsx
│   │   │   ├── PortfolioPage.tsx
│   │   │   └── AdminPage.tsx
│   │   ├── store/
│   │   │   └── useStore.ts    # Zustand store
│   │   ├── api/
│   │   │   └── client.ts      # API client
│   │   ├── types/
│   │   │   └── index.ts       # TypeScript типы
│   │   ├── styles/
│   │   │   └── index.css      # Tailwind config
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
├── docker-compose.yml
├── Dockerfile
└── .gitignore
```

## 🚀 Быстрый старт

### Локально (разработка)

```bash
# 1. Клонируем репозиторий
git clone https://github.com/RKP16102052/nft-gift-trading-bot.git
cd nft-gift-trading-bot

# 2. Backend
cd backend
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt

# 3. Настраиваем .env
cp .env.example .env
# Заполняем BOT_TOKEN (от @BotFather)

# 4. Запускаем
python -m app.main

# 5. Frontend (новый терминал)
cd frontend
npm install
npm run dev
```

### Docker (production)

```bash
docker-compose up --build
```

## 🔧 Конфигурация

Создайте `backend/.env`:

```env
BOT_TOKEN=your_bot_token_here
WEBAPP_URL=https://your-domain.com
DATABASE_URL=sqlite:///./nft_trading.db
DEBUG=False
ADMIN_ID=your_telegram_id
```

## 📊 API Endpoints

### NFT
- `GET /api/nft/list` - Список всех NFT
- `GET /api/nft/{id}` - Детали NFT
- `GET /api/nft/{id}/price-history` - История цен
- `POST /api/nft/create` - Создать NFT (админ)

### User
- `GET /api/user/me` - Текущий пользователь
- `POST /api/user/register` - Регистрация
- `GET /api/user/portfolio` - Портфель
- `POST /api/user/add-balance` - Добавить баланс

### Market
- `GET /api/market/listings` - Активные листинги
- `POST /api/market/sell` - Выставить на продажу
- `POST /api/market/cancel` - Отменить продажу
- `POST /api/market/buy` - Купить NFT
- `GET /api/market/orders` - История ордеров

### Prices
- `GET /api/prices/history/{nft_id}` - История цен за период
- `GET /api/prices/stats` - Статистика по NFT

## 🎨 Дизайн

- **Основной цвет**: Розовый (#EC4899)
- **Тема**: Modern, clean, трейдерская (как на бирже)
- **Компоненты**: Минималистичные карточки, графики, таблицы

## 📱 Telegram Команды

- `/start` - Начало работы (открыть WebApp)
- `/help` - Справка
- `/portfolio` - Мой портфель
- `/admin` - Админ-панель (только для админов)
- `/logs` - Скачать логи (админ)
- `/stats` - Статистика (админ)

## 🔐 Безопасность

- ✅ Верификация WebApp данных
- ✅ Валидация всех входных данных
- ✅ Rate limiting на API
- ✅ CORS контроль
- ✅ SQL injection protection (SQLAlchemy)

## 📈 Дальнейшее развитие

- [ ] Интеграция с TON блокчейном
- [ ] Push уведомления о изменении цен
- [ ] Расширенная аналитика
- [ ] Реферальная программа
- [ ] Система рейтингов трейдеров
- [ ] Автотрейдинг (боты)

## 📞 Контакты

Телеграм: @ADeri_RLP
GitHub: https://github.com/RKP16102052

## 📄 Лицензия

MIT
