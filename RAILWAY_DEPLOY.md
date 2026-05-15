# Развёртывание на Railway 🚀

## Предварительная подготовка

1. **Создайте аккаунт на Railway**: https://railway.app
2. **Установите Railway CLI**: https://docs.railway.app/guides/cli
3. **Получите Bot Token** от @BotFather в Telegram

## Шаги развёртывания

### 1. Инициализация Railway проекта

```bash
railway init
```

Выберите:
- Язык: Python
- Имя проекта: `nft-gift-trading-bot`

### 2. Добавьте переменные окружения

```bash
railway variables set BOT_TOKEN=your_bot_token_here
railway variables set WEBAPP_URL=your-app-url.railway.app
railway variables set ADMIN_ID=your_telegram_id
```

Получить URL приложения можно после первого деплоя:

```bash
railway domains
```

### 3. Развёртывание

```bash
railway up
```

Или через GitHub:
1. Загрузите репозиторий на GitHub
2. В Railway создайте новый проект
3. Подключите репозиторий
4. Добавьте переменные окружения
5. Railway автоматически развернёт приложение при каждом push

### 4. Настройте Telegram WebApp

Обновите `WEBAPP_URL` в переменных окружения на полный URL вашего приложения:

```bash
railway variables set WEBAPP_URL=https://your-app-name.railway.app
```

### 5. Проверка статуса

```bash
railway logs
```

## Мониторинг

```bash
# Просмотр логов в реальном времени
railway logs -f

# Просмотр статуса сервиса
railway status

# Обновление переменных
railway variables edit
```

## Проблемы и решения

### Бот не отвечает

1. Проверьте `BOT_TOKEN`: `railway logs`
2. Убедитесь, что `ADMIN_ID` установлен правильно
3. Перезагрузите сервис: `railway redeploy`

### WebApp не открывается

1. Проверьте `WEBAPP_URL` в переменных окружения
2. Убедитесь, что URL корректный и доступный
3. Очистите кэш браузера

### База данных не сохраняется

1. Railway использует ephemeral storage
2. Для production используйте PostgreSQL или MySQL
3. Добавьте сервис БД через Railway dashboard

## Production Чеклист

- [ ] Bot Token установлен правильно
- [ ] WEBAPP_URL указывает на правильный домен
- [ ] ADMIN_ID установлен
- [ ] Debug = False в production
- [ ] Логи настроены
- [ ] Резервная копия БД (для production)
- [ ] SSL сертификат (автоматически на Railway)
- [ ] Custom domain (опционально)

## Railway Dashboard

Откройте https://railway.app/dashboard чтобы:
- Просматривать логи
- Управлять переменными окружения
- Мониторить использование ресурсов
- Настраивать custom domains
- Просматривать историю развёртываний

## Дальнейшие улучшения

1. **PostgreSQL вместо SQLite** - для production
2. **Redis** - для кэширования и сессий
3. **S3/CloudStorage** - для хранения изображений NFT
4. **Monitoring** - настройка алертов
5. **CI/CD** - автоматическое тестирование при push
