# 📡 Обновление API Endpoints

## ✅ Что изменилось

### Новые endpoints:

1. **GET /stats** - Основная статистика (без онлайна)
2. **GET /stats/online** - Онлайн пользователи (отдельно)
3. **GET /servers/status** - Статус серверов

### Что удалено:

- ❌ Выручка за сегодня - больше не отображается

---

## 📊 API Endpoints

### 1. GET /stats

**URL:** `http://grushkin.ddns.net:25565/stats`

**Headers:**
```
Authorization: Bearer e1fleciEiLbK_etcBZTGGvV1aSXq_XL6ntxVbmYjCzs
```

**Response:**
```json
{
  "total_users": 1234,
  "active_subscriptions": 89,
  "today_transactions": 12,
  "today_new_users": 5
}
```

**Что используется:**
- `total_users` → 👤 Всего пользователей
- `active_subscriptions` → 🔑 Активные подписки
- `today_new_users` → 🆕 Новые пользователи сегодня

---

### 2. GET /stats/online

**URL:** `http://grushkin.ddns.net:25565/stats/online`

**Headers:**
```
Authorization: Bearer e1fleciEiLbK_etcBZTGGvV1aSXq_XL6ntxVbmYjCzs
```

**Response:**
```json
{
  "online_users": 42
}
```

или

```json
{
  "count": 42
}
```

**Что используется:**
- `online_users` или `count` → 👥 Пользователи онлайн

---

### 3. GET /servers/status

**URL:** `http://grushkin.ddns.net:25565/servers/status`

**Headers:**
```
Authorization: Bearer e1fleciEiLbK_etcBZTGGvV1aSXq_XL6ntxVbmYjCzs
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

**Что используется:**
- `servers[]` → 📊 Состояние серверов
- `country_name` → Название сервера
- `online` → true = 🟢 Online, false = 🔴 Offline

---

## 🎯 Что отображается на сайте

### VPN Service:

1. **👥 Пользователи онлайн**
   - Источник: `/stats/online`
   - Поле: `online_users` или `count`

2. **👤 Всего пользователей**
   - Источник: `/stats`
   - Поле: `total_users`

3. **🔑 Активные подписки**
   - Источник: `/stats`
   - Поле: `active_subscriptions`

4. **🆕 Новых сегодня**
   - Источник: `/stats`
   - Поле: `today_new_users`

5. **📊 Состояние серверов**
   - Источник: `/servers/status`
   - Поле: `servers[]`
   - Показывается максимум 3 сервера

---

## 🔧 Как работает

### Алгоритм загрузки:

```javascript
1. Запрос → /stats (основная статистика)
2. Запрос → /stats/online (онлайн пользователи)
3. Запрос → /servers/status (серверы)
4. Объединение данных
5. Отображение на сайте
```

### Обработка ошибок:

- Если `/stats/online` недоступен → онлайн = 0 (с предупреждением)
- Если `/servers/status` недоступен → показывается "Загрузка..."
- Если `/stats` недоступен → показывается "Offline"

---

## 🧪 Тестирование

### Проверка endpoints:

```bash
# 1. Основная статистика
curl -H "Authorization: Bearer e1fleciEiLbK_etcBZTGGvV1aSXq_XL6ntxVbmYjCzs" \
     http://grushkin.ddns.net:25565/stats

# 2. Онлайн пользователи
curl -H "Authorization: Bearer e1fleciEiLbK_etcBZTGGvV1aSXq_XL6ntxVbmYjCzs" \
     http://grushkin.ddns.net:25565/stats/online

# 3. Серверы
curl -H "Authorization: Bearer e1fleciEiLbK_etcBZTGGvV1aSXq_XL6ntxVbmYjCzs" \
     http://grushkin.ddns.net:25565/servers/status
```

### Проверка в браузере:

1. Откройте сайт: https://grush-in.github.io
2. Перейдите на "Сервисы" → "VPN Service"
3. Откройте консоль (F12)
4. Должно быть:
   ```
   ✅ VPN статистика загружена: {...}
   ```

---

## 📝 Что удалено

### Выручка за сегодня:

- ❌ Секция "💰 Выручка сегодня" удалена
- ❌ Поле `revenue_today` не используется
- ❌ Поле `today_transactions` не отображается
- ❌ Метр выручки удален

### Интерфейс теперь:

**Было (4 блока):**
```
[👥 Онлайн] [👤 Всего] [💰 Выручка] [📊 Серверы]
```

**Стало (3 блока):**
```
[👥 Онлайн] [🔑 Подписки] [📊 Серверы]
```

---

## 🎨 Адаптивность

### На широких экранах:
- 3 колонки в ряд

### На планшетах (< 940px):
- 1 колонка (все блоки друг под другом)

### На мобильных (< 768px):
- 1 колонка (компактный вид)

---

## ✅ Готово!

Теперь сайт использует правильные endpoints:

- ✅ `/stats` - основная статистика
- ✅ `/stats/online` - онлайн пользователи
- ✅ `/servers/status` - статус серверов
- ✅ Выручка удалена
- ✅ 3 блока вместо 4

**Проверьте что все работает!** 🚀

---

**Версия:** 2.1.1  
**Дата:** Октябрь 2025  
**Автор:** Grush-in Project

