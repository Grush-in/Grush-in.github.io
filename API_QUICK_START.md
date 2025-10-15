# ⚡ API Quick Start - Настройка за 1 минуту

## 🎯 Цель

Подключить сайт к вашему API серверу для получения реальных данных.

---

## 📋 Что нужно

- ✅ URL вашего API сервера (например: `http://grushkin.ddns.net:25565`)
- ✅ API токен для авторизации
- ✅ Работающие endpoints: `/stats` и `/servers/status`

---

## 🚀 Настройка (1 минута)

### Шаг 1: Откройте index.html

Найдите секцию **API Configuration** (примерно строка 1455):

```javascript
const API_CONFIG = {
  url: 'http://grushkin.ddns.net:25565',
  token: 'e1fleciEiLbK_etcBZTGGvV1aSXq_XL6ntxVbmYjCzs',
  useAPI: true
};
```

### Шаг 2: Замените на свои данные

```javascript
const API_CONFIG = {
  url: 'http://YOUR-SERVER:PORT',      // ← Ваш API URL
  token: 'YOUR_API_TOKEN_HERE',        // ← Ваш токен
  useAPI: true                         // ← true = использовать API
};
```

### Шаг 3: Сохраните и обновите страницу

- Сохраните файл `index.html`
- Обновите страницу в браузере (Ctrl+R)
- Готово! 🎉

---

## ✅ Проверка

### 1. Откройте сайт

Перейдите на вкладку **"Сервисы"** → **"VPN Service"**

### 2. Проверьте данные

Должны отображаться:
- 👥 Онлайн пользователей: **реальное число**
- 🔑 Активные подписки: **реальное число**
- 💰 Выручка: **реальная сумма**
- 🖥️ Статус серверов: **список серверов**

### 3. Проверьте консоль (F12)

Должно быть:
```
✅ VPN статистика загружена: {online_users: 42, ...}
```

---

## ❌ Если не работает

### Проблема: "Нет данных"

**Проверьте:**
1. ✅ API сервер запущен
2. ✅ URL правильный (с `http://` или `https://`)
3. ✅ Токен правильный
4. ✅ Endpoints `/stats` и `/servers/status` работают

**Откройте консоль (F12):**
```javascript
// Если видите ошибку:
❌ Ошибка API: Error: Failed to fetch

// Проверьте CORS на сервере!
```

### Проблема: "CORS error"

**Решение:**
На вашем API сервере добавьте CORS headers:

```python
# Python (FastAPI)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
)
```

### Проблема: "401 Unauthorized"

**Решение:**
- Проверьте токен в `API_CONFIG`
- Убедитесь что токен активен на сервере

---

## 🔄 Переключение на stats.json

Если хотите вернуться к GitHub Actions:

```javascript
const API_CONFIG = {
  url: 'http://grushkin.ddns.net:25565',
  token: 'e1fleciEiLbK_etcBZTGGvV1aSXq_XL6ntxVbmYjCzs',
  useAPI: false  // ← false = использовать stats.json
};
```

---

## 📡 Формат API

### Endpoint: GET /stats

**Response:**
```json
{
  "online_users": 42,
  "total_users": 1234,
  "active_subscriptions": 89,
  "today_revenue": 1234.56,
  "today_transactions": 12,
  "today_new_users": 5
}
```

### Endpoint: GET /servers/status

**Response:**
```json
{
  "servers": [
    {
      "country_name": "🇩🇪 Германия",
      "url": "https://de.vpn.com",
      "online": true
    }
  ]
}
```

---

## 🎉 Готово!

Теперь сайт получает данные с вашего API в реальном времени!

**Дополнительная информация:**
- 📚 `API_INTEGRATION.md` - Полная документация
- 🆕 `WHATS_NEW.md` - Что нового в версии 2.1.0

---

**Время настройки:** 1 минута  
**Сложность:** ⭐☆☆☆☆ (Очень легко)

