# VPN Stats API - Vercel Endpoint

API endpoint для приема и сохранения статистики от VPN бота в GitHub репозиторий.

## 🚀 Быстрый старт

### 1. Установка

```bash
cd vercel-api-example
npm install
```

### 2. Создайте GitHub Personal Access Token

1. Перейдите на https://github.com/settings/tokens
2. Нажмите "Generate new token (classic)"
3. Выберите права: **repo** (full control)
4. Сохраните токен в безопасном месте

### 3. Настройте переменные окружения

Скопируйте `.env.example` в `.env`:

```bash
cp .env.example .env
```

Отредактируйте `.env`:

```env
GITHUB_TOKEN=ghp_ваш_токен_сюда
STATS_API_KEY=ваш_секретный_ключ  # Опционально
```

### 4. Тестирование локально

```bash
npm run dev
```

API будет доступен на http://localhost:3000/api/stats

Тестовый запрос:
```bash
curl -X POST http://localhost:3000/api/stats \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ваш_секретный_ключ" \
  -d '{
    "app_name": "Test",
    "timestamp": "2025-10-11T15:30:00",
    "online_users": 5,
    "total_users": 100,
    "active_keys": 50,
    "revenue_today": 1000.0
  }'
```

### 5. Деплой на Vercel

```bash
# Первый раз
vercel login
vercel

# Продакшн деплой
npm run deploy
```

### 6. Настройте секреты в Vercel

После деплоя, добавьте секреты через Dashboard или CLI:

```bash
vercel env add GITHUB_TOKEN
vercel env add STATS_API_KEY
```

### 7. Обновите бота

В `.env` файле бота обновите:

```env
STATS_WEBSITE_URL=https://ваш-проект.vercel.app/api/stats
STATS_API_KEY=ваш_секретный_ключ
```

## 📋 API Документация

### POST /api/stats

Принимает статистику от бота и сохраняет в GitHub.

**Headers:**
```
Content-Type: application/json
Authorization: Bearer your_api_key  # Опционально
```

**Body:**
```json
{
  "app_name": "RunaVPN Bot",
  "timestamp": "2025-10-11T15:30:00.123456",
  "online_users": 42,
  "total_users": 1234,
  "active_keys": 89,
  "transactions_today": 12,
  "revenue_today": 1234.56,
  "new_users_today": 5,
  "uptime_seconds": 86400.0
}
```

**Success Response:**
```json
{
  "success": true,
  "message": "Stats updated successfully",
  "commit": "abc1234",
  "timestamp": "2025-10-11T15:30:00.000Z"
}
```

**Error Response:**
```json
{
  "error": "Unauthorized",
  "message": "Invalid API key",
  "timestamp": "2025-10-11T15:30:00.000Z"
}
```

## 🔧 Конфигурация

Отредактируйте `api/stats.js` для изменения:

```javascript
const GITHUB_OWNER = 'Grush-in';  // Ваш GitHub username
const GITHUB_REPO = 'Grush-in.github.io';  // Ваш репозиторий
const STATS_FILE_PATH = 'stats.json';  // Путь к файлу статистики
```

## 🛡️ Безопасность

- ✅ CORS настроен для работы с любым источником
- ✅ Опциональная авторизация через Bearer token
- ✅ Валидация входящих данных
- ✅ Безопасное хранение токенов в Vercel Secrets

## 📊 Мониторинг

Логи доступны в Vercel Dashboard:
- https://vercel.com/dashboard
- Выберите проект → Functions → Logs

## ❓ Troubleshooting

**Ошибка: "Unauthorized"**
- Проверьте что STATS_API_KEY совпадает в боте и на Vercel

**Ошибка: "Bad credentials"**
- Проверьте GITHUB_TOKEN
- Убедитесь что токен имеет права `repo`

**Статистика не обновляется на сайте**
- Проверьте что файл `stats.json` обновляется в GitHub
- Проверьте консоль браузера на наличие ошибок

## 📝 Лицензия

MIT


