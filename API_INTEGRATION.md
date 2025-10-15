# 🔌 API Integration - Подключение к серверу статистики

## ✨ Что добавлено

Теперь VPN Service может получать данные **напрямую с вашего API сервера** вместо `stats.json`!

### Возможности:

- 📊 **Реальные данные** - прямое подключение к API
- 🖥️ **Статус серверов** - показ состояния VPN серверов
- 🔄 **Автообновление** - каждые 10 секунд
- 🔐 **Авторизация** - Bearer token
- 🎯 **Два режима** - API сервер или stats.json

---

## 🚀 Быстрая настройка

### Вариант 1: Использовать API сервер (рекомендуется)

В `index.html` найдите секцию **API Configuration** (примерно строка 1455):

```javascript
const API_CONFIG = {
  url: 'http://grushkin.ddns.net:25565',  // ← Ваш API URL
  token: 'e1fleciEiLbK_etcBZTGGvV1aSXq_XL6ntxVbmYjCzs',  // ← Ваш API токен
  useAPI: true  // true = API сервер, false = stats.json
};
```

**Измените на свои данные:**

```javascript
const API_CONFIG = {
  url: 'http://your-server.com:port',  // Ваш сервер
  token: 'your_api_token_here',        // Ваш токен
  useAPI: true
};
```

### Вариант 2: Использовать stats.json (GitHub Actions)

```javascript
const API_CONFIG = {
  url: 'http://grushkin.ddns.net:25565',
  token: 'e1fleciEiLbK_etcBZTGGvV1aSXq_XL6ntxVbmYjCzs',
  useAPI: false  // ← Установите false
};
```

---

## 📡 API Endpoints

Ваш API сервер должен предоставлять следующие endpoints:

### 1. GET /stats

**Описание:** Основная статистика VPN сервиса

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json
```

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

### 2. GET /servers/status

**Описание:** Статус VPN серверов

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json
```

**Response:**
```json
{
  "servers": [
    {
      "country_name": "🇩🇪 Германия",
      "url": "https://de.vpn.com:2053",
      "online": true
    },
    {
      "country_name": "🇳🇱 Нидерланды",
      "url": "https://nl.vpn.com:2053",
      "online": true
    }
  ]
}
```

---

## 🎨 Отображение на сайте

### Статистика

Автоматически преобразуется в нужный формат:

```javascript
API Response          →    Отображение на сайте
online_users          →    👥 Онлайн пользователей
total_users           →    👤 Всего пользователей
active_subscriptions  →    🔑 Активные подписки
today_revenue         →    💰 Выручка сегодня
today_transactions    →    📊 Транзакции
today_new_users       →    🆕 Новые пользователи
```

### Серверы

Показываются максимум **3 первых сервера** с индикаторами:
- 🟢 Зеленый = Online
- 🔴 Красный = Offline

Если серверов больше 3, показывается счетчик:
```
Всего серверов: 5 (онлайн: 4)
```

---

## 🔧 Конфигурация

### Изменить URL API

```javascript
const API_CONFIG = {
  url: 'http://your-new-server.com:8080',  // ← Ваш URL
  token: 'your_token',
  useAPI: true
};
```

### Изменить токен авторизации

```javascript
const API_CONFIG = {
  url: 'http://grushkin.ddns.net:25565',
  token: 'new_token_123456',  // ← Новый токен
  useAPI: true
};
```

### Переключиться на stats.json

```javascript
const API_CONFIG = {
  url: 'http://grushkin.ddns.net:25565',
  token: 'e1fleciEiLbK_etcBZTGGvV1aSXq_XL6ntxVbmYjCzs',
  useAPI: false  // ← false = использовать stats.json
};
```

---

## 🧪 Тестирование

### Проверка подключения к API

Откройте консоль браузера (F12) и проверьте:

```javascript
// Успешное подключение:
✅ VPN статистика загружена: {online_users: 42, ...}

// Ошибка подключения:
❌ Ошибка API: Error: HTTP 401: Unauthorized
```

### Тест авторизации

Если видите ошибку `401 Unauthorized`:
1. Проверьте что токен правильный
2. Убедитесь что токен активен
3. Проверьте формат: `Bearer YOUR_TOKEN`

### Тест endpoints

Проверьте вручную в браузере или Postman:

```bash
# Тест /stats
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://grushkin.ddns.net:25565/stats

# Тест /servers/status
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://grushkin.ddns.net:25565/servers/status
```

---

## 🔒 Безопасность

### CORS

Ваш API сервер должен разрешать CORS запросы:

```javascript
// Пример для Express.js
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Authorization, Content-Type');
  next();
});
```

### HTTPS

⚠️ **Важно:** Для продакшена используйте HTTPS вместо HTTP!

```javascript
const API_CONFIG = {
  url: 'https://your-server.com',  // ← HTTPS!
  token: 'your_token',
  useAPI: true
};
```

### Токен

- 🔐 Храните токен в безопасности
- 🔄 Регулярно меняйте токен
- ❌ Не публикуйте токен в публичных репозиториях

---

## 📊 Преимущества API

### По сравнению со stats.json:

**Плюсы:**
- ✅ Реальные данные в реальном времени
- ✅ Статус серверов
- ✅ Не нужен GitHub Actions
- ✅ Мгновенное обновление

**Минусы:**
- ⚠️ Требуется работающий API сервер
- ⚠️ Нужна настройка CORS
- ⚠️ Зависимость от сервера

---

## 🔄 Как работает

```
1. Сайт делает запрос → API_CONFIG.url/stats
                          ↓
2. API проверяет токен → Authorization: Bearer TOKEN
                          ↓
3. API возвращает данные → JSON response
                          ↓
4. Сайт преобразует формат → stats объект
                          ↓
5. Обновляется отображение → VPN Service
```

**Интервал проверки:** каждые 10 секунд

---

## ❌ Troubleshooting

### Проблема: "Нет данных"

**Причины:**
1. API сервер не работает
2. Неправильный URL
3. Неправильный токен
4. CORS блокирует запросы

**Решение:**
1. Проверьте что API сервер запущен
2. Проверьте URL в API_CONFIG
3. Проверьте токен
4. Настройте CORS на сервере
5. Проверьте консоль браузера (F12) на ошибки

### Проблема: "CORS error"

```
Access to fetch at '...' from origin '...' has been blocked by CORS policy
```

**Решение:**
Добавьте CORS headers на вашем API сервере.

### Проблема: "401 Unauthorized"

**Решение:**
1. Проверьте токен в API_CONFIG
2. Убедитесь что токен активен на сервере
3. Проверьте формат авторизации

### Проблема: "Серверы не отображаются"

**Решение:**
1. Проверьте endpoint `/servers/status`
2. Убедитесь что формат ответа правильный
3. Проверьте консоль на ошибки

---

## 🎯 Рекомендации

### Для продакшена:

1. ✅ Используйте HTTPS
2. ✅ Настройте правильный CORS
3. ✅ Регулярно обновляйте токен
4. ✅ Мониторьте API сервер
5. ✅ Настройте fallback на stats.json

### Для разработки:

1. 🛠 Используйте HTTP (локально)
2. 🛠 Разрешите все CORS
3. 🛠 Используйте тестовый токен
4. 🛠 Проверяйте консоль браузера

---

## 📝 Пример настройки API сервера

### Python (FastAPI)

```python
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_TOKEN = "e1fleciEiLbK_etcBZTGGvV1aSXq_XL6ntxVbmYjCzs"

def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Unauthorized")
    
    token = authorization.replace("Bearer ", "")
    if token != API_TOKEN:
        raise HTTPException(401, "Invalid token")

@app.get("/stats")
async def get_stats(auth: str = Depends(verify_token)):
    return {
        "online_users": 42,
        "total_users": 1234,
        "active_subscriptions": 89,
        "today_revenue": 1234.56,
        "today_transactions": 12,
        "today_new_users": 5
    }

@app.get("/servers/status")
async def get_servers(auth: str = Depends(verify_token)):
    return {
        "servers": [
            {
                "country_name": "🇩🇪 Германия",
                "url": "https://de.vpn.com",
                "online": True
            }
        ]
    }
```

---

## 🎉 Готово!

Теперь VPN Service получает данные с вашего API сервера в реальном времени!

**Что дальше:**
1. ✅ Настройте API_CONFIG
2. ✅ Проверьте подключение
3. ✅ Настройте CORS (если нужно)
4. ✅ Наслаждайтесь реальными данными!

---

**Версия:** 2.1.0  
**Дата:** Октябрь 2025  
**Автор:** Grush-in Project

